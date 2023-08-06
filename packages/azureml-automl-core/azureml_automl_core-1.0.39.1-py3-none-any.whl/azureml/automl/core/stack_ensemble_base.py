# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base module for ensembling previous AutoML iterations."""

from abc import ABC
import json
import numpy as np
import typing
from sklearn import base
from sklearn import linear_model
from sklearn import model_selection

from automl.client.core.common import constants
from automl.client.core.common import model_wrappers
from automl.client.core.common import pipeline_spec as pipeline_spec_module
from . import ensemble_base


class StackEnsembleBase(ensemble_base.EnsembleBase, ABC):
    """
    Class for creating a Stacked Ensemble based on previous AutoML iterations.

    The ensemble pipeline is initialized from a collection of already fitted pipelines.
    """

    def __init__(self, automl_settings):
        """Create an Ensemble pipeline out of a collection of already fitted pipelines.

        :param automl_settings: settings for the AutoML experiments.
        """
        super(StackEnsembleBase, self).__init__(automl_settings)

    def _create_ensembles(self, logger, fitted_pipelines, selector):
        logger.info("Creating a Stack Ensemble out of iterations: {}".format(selector.unique_ensemble))

        if selector.training_type == constants.TrainingType.TrainAndValidation:
            return self._create_stack_ensembles_train_validation(logger,
                                                                 fitted_pipelines,
                                                                 selector)
        elif selector.training_type == constants.TrainingType.MeanCrossValidation:
            return self._create_stack_ensembles_cross_validation(logger,
                                                                 fitted_pipelines,
                                                                 selector)
        else:
            raise ValueError("Unsupported training type ({})".format(selector.training_type))

    def _create_stack_ensembles_train_validation(self,
                                                 logger,
                                                 fitted_pipelines,
                                                 selector):
        # for this type of training, we need the meta_model to be trained on the predictions
        # over the validation set from all the base learners.
        # This will be the ensemble returned for predictions on new data.
        _, y_valid, sample_weight_valid = selector.dataset.get_valid_set()
        all_prediction_list = []
        base_learners_tuples = []
        pipeline_specs = []
        for model_index in selector.unique_ensemble:
            base_learners_tuples.append(
                (str(fitted_pipelines[model_index][self.PIPELINES_TUPLES_ITERATION_INDEX]),
                 fitted_pipelines[model_index][self.PIPELINES_TUPLES_PIPELINE_INDEX]))
            pipeline_specs.append(fitted_pipelines[model_index][self.PIPELINES_TUPLES_PIPELINE_SPEC_INDEX])
            model_predictions = selector.predictions[:, :, model_index]
            # for regression we need to slice the matrix becauase there's a single "class" in the second dimension
            if selector.task_type == constants.Tasks.REGRESSION:
                model_predictions = model_predictions[:, 0]
            all_prediction_list.append(model_predictions)

        meta_learner_training_set = model_wrappers.StackEnsembleBase._horizontal_concat(all_prediction_list)
        meta_learner, meta_learner_supports_sample_weights = self._create_meta_learner()

        self._fit_meta_learner(
            meta_learner, meta_learner_training_set, y_valid,
            sample_weight_valid, meta_learner_supports_sample_weights)

        fully_fitted_stack_ensemble = self._create_stack_ensemble(base_learners_tuples, meta_learner)

        problem_info = selector.dataset.get_problem_info()

        # We'll need to retrain the base learners pipelines on 80% (the default) of the training set
        # and we'll use the remaining 20% to generate out of fold predictions which will
        # represent the input training set of the meta_learner.
        X_train, y_train, sample_weight_train = selector.dataset.get_train_set()
        scoring_meta_learner = base.clone(meta_learner)
        self._train_scoring_ensemble_for_train_validate(
            X_train, y_train, sample_weight_train, problem_info, selector.task_type,
            pipeline_specs, scoring_meta_learner, meta_learner_supports_sample_weights)

        # after we've trained the meta learner, we can reuse the fully trained base learners (on 100% of train set)
        scoring_stack_ensemble = self._create_stack_ensemble(base_learners_tuples, scoring_meta_learner)
        return fully_fitted_stack_ensemble, scoring_stack_ensemble

    def _create_stack_ensembles_cross_validation(self,
                                                 logger,
                                                 fitted_pipelines,
                                                 selector):
        # we'll need to fetch the fully fitted models for the models that will be part of the base learners
        # so far the selection algo has been using the partially fitted ones for each AUTO ML iteration
        fully_fitted_learners_tuples = self._create_fully_fitted_ensemble_estimator_tuples(logger,
                                                                                           fitted_pipelines,
                                                                                           selector.unique_ensemble)
        # fully_fitted_learners_tuples represents a list of tuples (iteration, fitted_pipeline)
        y_valid_full = selector.y_valid
        sample_weights_valid_full = selector.sample_weight_valid

        all_out_of_fold_predictions = []
        for model_index in selector.unique_ensemble:
            # get the vertical concatenation of the out of fold predictions from the selector
            # as they were already computed during the selection phase
            model_predictions = selector.predictions[:, :, model_index]
            if selector.task_type == constants.Tasks.REGRESSION:
                model_predictions = model_predictions[:, 0]
            all_out_of_fold_predictions.append(model_predictions)
        meta_learner_training = model_wrappers.StackEnsembleBase._horizontal_concat(all_out_of_fold_predictions)

        meta_learner, meta_learner_supports_sample_weights = self._create_meta_learner()
        self._fit_meta_learner(
            meta_learner, meta_learner_training, y_valid_full,
            sample_weights_valid_full, meta_learner_supports_sample_weights)

        fully_fitted_stack_ensemble = self._create_stack_ensemble(fully_fitted_learners_tuples, meta_learner)

        # Now we need to construct some Stack Ensembles to be used for computing the metric scores
        # we'll need to keep one fold out (holdout) from the CV folds and concatenate vertically those predictions.
        # The vertical concatenation has already happened within the EnsembleSelector.
        # The concatenated predictions will be used for training the meta model in a CV fashion
        # then we'll create a StackedEnsemble where the base learners are the partially fitted models
        # from the selected AutoML iteration which haven't seen the holdout set.
        # Again, we'll reuse the selector.predictions matrix along with the row ranges corresponding to each fold,
        # excluding each time a different range
        cross_validated_stack_ensembles = []
        # get the CV indices from selector
        # this represents the range of indices within the predictions matrix which contains
        # the partial model's (corresponding to this training fold) predictions on y_valid.
        for fold_index, cv_indices in enumerate(selector.cross_validate_indices):
            base_learners_tuples = []
            stacker_training_set = []
            # Fetch each train/validation fold from the CV splits. this will be used for training of the stacker.
            # The ensemble selector keeps track of the ranges of row indices that correspond to each out of fold
            # predictions slice within the selector.predictions matrix.
            # Here, cv_indices is an interval represented through a tuple(row_index_start, row_index_end).
            slice_to_exclude_from_predictions = range(cv_indices[0], cv_indices[1])
            for counter, model_index in enumerate(selector.unique_ensemble):
                # get the partially fitted model that hasn't been trained on this holdout set
                # this will be used as base learner for this scoring StackEnsemble
                base_learners_tuples.append(
                    (str(fitted_pipelines[model_index][self.PIPELINES_TUPLES_ITERATION_INDEX]),
                     fitted_pipelines[model_index][self.PIPELINES_TUPLES_PIPELINE_INDEX][fold_index]))
                # we'll grab all the out of fold predictions for this model excluding the holdout set.
                # these predictions will be used as training data for the meta_learner
                stacker_training_set.append(
                    np.delete(all_out_of_fold_predictions[counter],
                              slice_to_exclude_from_predictions, axis=0))
            # create the meta learner model and then fit it
            scoring_meta_learner = base.clone(meta_learner)
            meta_learner_training_set = model_wrappers.StackEnsembleBase._horizontal_concat(stacker_training_set)
            y_train_fold = np.delete(selector.y_valid, slice_to_exclude_from_predictions)
            if selector.sample_weight_valid is not None:
                sample_weights_train_fold = np.delete(selector.sample_weight_valid, slice_to_exclude_from_predictions)
            else:
                sample_weights_train_fold = None

            self._fit_meta_learner(
                scoring_meta_learner,
                meta_learner_training_set, y_train_fold,
                sample_weights_train_fold, meta_learner_supports_sample_weights)

            scoring_stack_ensemble = self._create_stack_ensemble(base_learners_tuples, scoring_meta_learner)

            if selector.task_type == constants.Tasks.CLASSIFICATION:
                # For cases when the base learner predictions have been padded so that all CV models have the same
                # shape, we'll have to ensure the StackEnsemble is aware of all classes involved in the padding.
                # For that, we'll have to override the classes_ attribute so that when later predicting, it'll apply
                # the same padding logic as it was applied during training.
                scoring_stack_ensemble.classes_ = fully_fitted_stack_ensemble.classes_

            cross_validated_stack_ensembles.append(scoring_stack_ensemble)

        return fully_fitted_stack_ensemble, cross_validated_stack_ensembles

    def _train_scoring_ensemble_for_train_validate(self, X, y, sample_weight, problem_info, task_type,
                                                   base_learners_pipeline_specs, meta_learner,
                                                   meta_learner_supports_sample_weights):
        meta_learner_train_percentage = constants.EnsembleConstants.DEFAULT_TRAIN_PERCENTAGE_FOR_STACK_META_LEARNER
        if hasattr(self._automl_settings, "stack_meta_learner_train_percentage"):
            meta_learner_train_percentage = float(self._automl_settings.stack_meta_learner_train_percentage)

        stratify = y if task_type == constants.Tasks.CLASSIFICATION else None

        sample_weight_meta_train = None
        if sample_weight is not None:
            try:
                X_base_train, X_meta_train, y_base_train, y_meta_train, _, sample_weight_meta_train =\
                    model_selection.train_test_split(
                        X, y, sample_weight, test_size=meta_learner_train_percentage, stratify=stratify)
            except ValueError:
                # in case stratification fails, fall back to non-stratify train/test split
                X_base_train, X_meta_train, y_base_train, y_meta_train, _, sample_weight_meta_train =\
                    model_selection.train_test_split(
                        X, y, sample_weight, test_size=meta_learner_train_percentage, stratify=None)
        else:
            try:
                X_base_train, X_meta_train, y_base_train, y_meta_train =\
                    model_selection.train_test_split(X, y, test_size=meta_learner_train_percentage, stratify=stratify)
            except ValueError:
                # in case stratification fails, fall back to non-stratify train/test split
                X_base_train, X_meta_train, y_base_train, y_meta_train =\
                    model_selection.train_test_split(X, y, test_size=meta_learner_train_percentage, stratify=None)

        scoring_base_learners = self._instantiate_pipelines_from_specs(base_learners_pipeline_specs, problem_info)

        for scoring_base_learner in scoring_base_learners:
            scoring_base_learner.fit(X_base_train, y_base_train)
        if task_type == constants.Tasks.CLASSIFICATION:
            # use the predict probabilities to return the class because the meta_learner was trained on probabilities
            predictions = [estimator.predict_proba(X_meta_train) for estimator in scoring_base_learners]
            concat_predictions = model_wrappers.StackEnsembleBase._horizontal_concat(predictions)
        else:
            predictions = [estimator.predict(X_meta_train) for estimator in scoring_base_learners]
            concat_predictions = model_wrappers.StackEnsembleBase._horizontal_concat(predictions)

        self._fit_meta_learner(
            meta_learner, concat_predictions, y_meta_train,
            sample_weight_meta_train, meta_learner_supports_sample_weights)

    def _create_meta_learner(self):
        meta_learner_ctor = None  # type: typing.Union[typing.Any, typing.Callable[..., typing.Any]]
        meta_learner_kwargs = {}  # type: typing.Dict[str, typing.Any]
        meta_learner_supports_sample_weights = True

        meta_learner_type = None
        if not hasattr(self._automl_settings, "stack_meta_learner_type"):
            if self._automl_settings.task_type == constants.Tasks.CLASSIFICATION:
                meta_learner_type = constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LogisticRegression
            else:
                meta_learner_type = constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.ElasticNet
        else:
            meta_learner_type = self._automl_settings.stack_meta_learner_type

        if meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LightGBMClassifier:
            meta_learner_ctor = model_wrappers.LightGBMClassifier
            meta_learner_kwargs = {"min_child_samples": 10}
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LightGBMRegressor:
            meta_learner_ctor = model_wrappers.LightGBMRegressor
            meta_learner_kwargs = {"min_child_samples": 10}
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LogisticRegression:
            meta_learner_ctor = linear_model.LogisticRegression
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LogisticRegressionCV:
            meta_learner_ctor = linear_model.LogisticRegressionCV
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.LinearRegression:
            meta_learner_ctor = linear_model.LinearRegression
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.ElasticNet:
            meta_learner_ctor = linear_model.ElasticNet
            meta_learner_supports_sample_weights = False
        elif meta_learner_type == constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.ElasticNetCV:
            meta_learner_ctor = linear_model.ElasticNetCV
            meta_learner_supports_sample_weights = False
        else:
            err = "{} is not supported as a model type for the Stack Meta Learner. Currently supported list: {}"\
                .format(
                    self._automl_settings.stack_meta_learner_type,
                    constants.EnsembleConstants.StackMetaLearnerAlgorithmNames.ALL)
            raise ValueError(err)

        if hasattr(self._automl_settings, "stack_meta_learner_kwargs") \
                and self._automl_settings.stack_meta_learner_kwargs is not None:
            meta_learner_kwargs = self._automl_settings.stack_meta_learner_kwargs

        return (meta_learner_ctor(**meta_learner_kwargs), meta_learner_supports_sample_weights)

    def _create_stack_ensemble(self, base_layer_tuples, meta_learner):
        result = None
        if self._automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            result = model_wrappers.StackEnsembleClassifier(base_learners=base_layer_tuples, meta_learner=meta_learner)
        else:
            result = model_wrappers.StackEnsembleRegressor(base_learners=base_layer_tuples, meta_learner=meta_learner)
        return result

    @staticmethod
    def _fit_meta_learner(meta_learner, X, y, sample_weight, learner_supports_sample_weights):
        if learner_supports_sample_weights:
            meta_learner.fit(X, y, sample_weight=sample_weight)
        else:
            meta_learner.fit(X, y)
        return meta_learner

    @staticmethod
    def _instantiate_pipelines_from_specs(pipeline_specs, problem_info):
        pipelines = []
        for spec in pipeline_specs:
            pipeline_dict = json.loads(spec)
            spec_obj = pipeline_spec_module.PipelineSpec.from_dict(pipeline_dict)
            pipeline = spec_obj.instantiate_pipeline_spec(problem_info)
            pipelines.append(pipeline)
        return pipelines
