# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Decompose the target value to the Trend and Seasonality."""
from typing import Optional, Any, Tuple, List, Callable, Union, Dict, Iterator, cast
from itertools import product
import warnings

from pandas.tseries.frequencies import to_offset
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose, DecomposeResult
from statsmodels.tsa.holtwinters import HoltWintersResultsWrapper
import numpy as np
import pandas as pd

from automl.client.core.common.constants import TimeSeriesInternal
from automl.client.core.common.exceptions import DataException, ConfigException
from automl.client.core.common.forecasting_exception import NotSupportedException
from automl.client.core.common.forecasting_ts_utils import detect_seasonality
from automl.client.core.common.forecasting_utils import get_period_offsets_from_dates, grain_level_to_dict
from automl.client.core.common.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.core.featurization.timeseries.forecasting_base_estimator import AzureMLForecastTransformerBase
from azureml.automl.core.featurization.timeseries.time_series_imputer import TimeSeriesImputer


def _complete_short_series(series_values: pd.Series,
                           season_len: int) -> Union[np.ndarray, pd.Series]:
    """
    Complete the two seasons required by statsmodels.

    statsmodels requires at least two full seasons of data
    in order to train. "Complete" the data if this requirement
    is not met.
    If there is less than one full season, carry the last observation
    forward to complete a full season.
    Use a seasonal naive imputation to fill in series values
    so the completed series has length at least 2*season_len
    :param series_values: The series with data.
    :type series_values: pd.Series
    :param season_len: The number of periods in the season.
    :type season_len: int
    :returns: the array with extended data or pd.Series.
    :rtype: np.ndarray pr pd.Series

    """
    series_len = len(series_values)

    # Nothing to do if we already have at least two seasons of data
    if series_len >= 2 * season_len:
        return series_values

    if series_len < season_len:
        last_obs = series_values[-1]
        one_season_ext = np.repeat(last_obs, season_len - series_len)
    else:
        one_season_ext = np.array([])

    # Complete a full season
    series_values_ext = np.append(series_values, one_season_ext)

    # Complete the second season via seasonal naive imputation
    num_past_season = len(series_values_ext) - season_len
    series_first_season = series_values_ext[:season_len]
    series_snaive_second_season = series_first_season[num_past_season:]

    # Get the final bit of the series by seasonal naive imputation
    series_snaive_end = series_values_ext[season_len:]

    # Concatenate all the imputations and return
    return np.concatenate((series_values_ext,
                           series_snaive_second_season,
                           series_snaive_end))


def _sm_is_ver9() -> bool:
    """
    Try to determine if the statsmodels version is 0.9.x.

    :returns: True if the statsmodels is of 0.9.x version.
    :rtype: bool

    """
    try:
        import pkg_resources
        sm_ver = pkg_resources.get_distribution('statsmodels').version
        major, minor = sm_ver.split('.')[:2]
        if major == '0' and minor == '9':
            return True
    except BaseException:
        return True

    return False


def _extend_series_for_sm9_bug(series_values: np.ndarray,
                               season_len: int,
                               model_type: Tuple[str, str, bool]) -> np.ndarray:
    """
    Fix the statsmodel 0.9.0 bug.

    statsmodel 0.9.0 has a bug that causes division by zero during
    model fitting under the following condition:
    series_length = num_model_params + 3.
    Try to detect this condition and if it is found, carry the last
    observation forward once in order to increase the series length.
    This bug is fixed in the (dev) version 0.10.x.
    :param series_values: the series with data.
    :type series_values: np.ndarray
    :param season_len: The number of periods in the season.
    :type season_len: int
    :param model_type: The type of a model used.
    :type model_type: tuple

    """
    trend_type, seas_type, damped = model_type
    num_params = 2 + 2 * (trend_type != 'N') + 1 * (damped) + \
        season_len * (seas_type != 'N')

    if len(series_values) == num_params + 3:
        series_ext = np.append(series_values, series_values[-1])
    else:
        series_ext = series_values

    return series_ext


class STLFeaturizer(AzureMLForecastTransformerBase):
    """
    The class for decomposition of input data to the seasonal and trend component.

    If seasonality is not presented by int or np.int64 ConfigException is raised.
    :param seasonality: Time series seasonality. If seasonality is set to -1, it will be inferred.
    :type seasonality: int
    :param model_type:
        str {"additive"(default), "multiplicative"}
        Type of seasonal component. Abbreviations are accepted.
    :type model_type: str
    :raises: ConfigException

    """

    def __init__(self,
                 seasonality: int = -1,
                 model_type: str = 'additive') -> None:
        """Constructor."""
        self._model_type = model_type
        if not isinstance(seasonality, int):
            raise ConfigException("The seasonality should be an integer.")
        self._seasonality = seasonality
        self._stls = {}  # type: Dict[Tuple[str], DecomposeResult]
        self._es_models = {}  # type: Dict[Tuple[str], HoltWintersResultsWrapper]
        # The parameters of ETS model. Currently they are not exposed.
        self.use_boxcox = False
        self.use_basinhopping = False
        self.damped = False
        self.selection_metric = 'aic'
        self._char_to_statsmodels_opt = \
            {'A': 'add', 'M': 'mul', 'N': None}
        self._freq = 0
        self._first_observation_dates = {}  # type: Dict[Tuple[str], pd.Timestamp]
        self._last_observation_dates = {}  # type: Dict[Tuple[str], pd.Timestamp]
        self._sm9_bug_workaround = _sm_is_ver9()
        self._ts_value = None  # Optional[str]

    def data_check(self, X: TimeSeriesDataFrame) -> None:
        """
        Perform data check before transform will be called.

        If the data are not valid the DataException is being raised.
        :param X: The TimeSeriesDataFrame with data to be transformed.
        :type X: TimeSeriesDataFrame
        :raises: DataException
        """
        for grain, df_one in X.groupby_grain():
            if grain not in self._last_observation_dates.keys() or \
               grain not in self._first_observation_dates.keys():
                raise DataException('The grain {} is not in the training set.'.format(grain))
            if df_one.time_index.min() < self._first_observation_dates[grain]:
                raise DataException('The forecast date cannot be less then training date.')

    def _get_imputed_df(self, X: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Impute the missing y values.

        :param X: Input data
        :type X: :class:`TimeSeriesDataFrame`
        :rtype: TimeIndexFeaturizer

        """
        # Imopute values by forward fill the values.
        imputer = TimeSeriesImputer(input_column=X.ts_value_colname,
                                    option='fillna',
                                    method='ffill',
                                    freq=self._freq)
        # We forward filled values at the middle and at the end
        # of a data frame. We will fill the begin with zeroes.
        zero_imputer = TimeSeriesImputer(input_column=X.ts_value_colname,
                                         value=0,
                                         freq=self._freq)
        imputed_X = imputer.transform(X)
        return cast(TimeSeriesDataFrame, zero_imputer.transform(imputed_X))

    def fit(self,
            X: TimeSeriesDataFrame,
            y: Optional[np.ndarray] = None) -> 'STLFeaturizer':
        """
        Determine trend and seasonality.

        If the number of rows is <= seasonality, the DataException is raised.
        :param X: Input data
        :type X: :class:`TimeSeriesDataFrame`
        :param y: Not used, added for back compatibility with scikit**-**learn.
        :type y: np.ndarray
        :return: Fitted transform
        :rtype: TimeIndexFeaturizer
        :raises: DataException

        """
        if X.origin_time_colname is not None:
            raise NotSupportedException('The time series data frames with origin times are not supported.')
        self._ts_value = X.ts_value_colname
        self._freq = X.infer_freq()

        # We have to impute missing values for correct
        # of seasonality detection.
        imputed_X = self._get_imputed_df(X)

        if self.seasonality == -1:
            self._seasonality = self.infer_seasonality(imputed_X)

        if self.seasonality >= imputed_X.shape[0]:
            raise DataException("Each grain of the training data set "
                                "should have more rows than seasonality.")

        self._apply_func_to_grains(self._fit_one_grain, imputed_X)
        return self

    def transform(self,
                  X: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Create time index features for an input data frame.

        **Note** in this method we assume that we do not know the target value.
        :param X: Input data
        :type X: :class:`ftk.time_series_data_frame.TimeSeriesDataFrame`
        :return: Data frame with trand and seasonality column.
        :rtype: :class:`ftk.time_series_data_frame.TimeSeriesDataFrame`
        :raises: Exception
        """
        if not self._stls.keys() or self.seasonality == -1:
            raise DataException("Fit not called")
        self.data_check(X)
        return self._apply_func_to_grains(self._transform_one_grain, X)

    def fit_transform(self,
                      X: TimeSeriesDataFrame,
                      y: Optional[np.ndarray] = None) -> TimeSeriesDataFrame:
        """
        Apply `fit` and `transform` methods in sequence.

        **Note** that because in this case we know the target value
        and hence we can use the statsmodel of trend inference.
        :param X: Input data.
        :type X: :class:`ftk.time_series_data_frame.TimeSeriesDataFrame`
        :param y: Not used, added for back compatibility with scikit**-**learn.
        :type y: np.ndarray
        :return: Data frame with trand and seasonality column.
        :rtype: :class:`ftk.time_series_data_frame.TimeSeriesDataFrame`

        """
        self.fit(X)
        return self._apply_func_to_grains(self._fit_transform_one_grain, X)

    def preview_column_names(self,
                             tsdf: Optional[TimeSeriesDataFrame] = None,
                             target: Optional[str] = None) -> List[str]:
        """
        Return the list of columns to be generated based on data in the data frame X.

        TimeSeriesDataFrame or target column, but not both should be provided.
        If neither or both are provided the DataException is raised.
        :param tsdf: The TimeSeriesDataFrame to generate column names for.
        :type tsdf: TimeSeriesDataFrame
        :param target: The name of a target column.
        :type target: str
        :returns: the list of generated columns.
        :rtype: list
        :raises: DataException

        """
        if (tsdf is None and target is None) or\
           (tsdf is not None and target is not None):
            raise DataException('tsdf or or target, but not both should be provided.')
        if tsdf is not None:
            return list(self._get_column_names(tsdf.ts_value_colname))
        # if target is not None:
        return list(self._get_column_names(cast(str, target)))

    def infer_seasonality(self, X: TimeSeriesDataFrame) -> int:
        """
        Return the seasonality of the data.

        If different grains have different seasonality the warning is shown and
        the most frequent seasonality will be returned.
        :param X: The dataset.
        :type X: TimeSeriesDataFrame
        :returns: The seasonality.
        :rtype: int

        """
        # seasonality->number of grains with it.
        seasonality_dict = {}  # type: Dict[int, int]
        dom_seasonality = -1
        max_series = 0
        for grain, df_one in X.groupby_grain():
            seasonality = detect_seasonality(df_one.ts_value)
            if seasonality not in seasonality_dict:
                seasonality_dict[seasonality] = 0
            seasonality_dict[seasonality] += 1
            if seasonality_dict[seasonality] > max_series:
                max_series = seasonality_dict[seasonality]
                dom_seasonality = seasonality
        if len(seasonality_dict.keys()) > 1:
            warnings.warn(
                'Different grains have different seasonality, '
                'the mode seasonality of {} will be used.'.format(seasonality))
        return dom_seasonality

    def _fit_one_grain(self,
                       grain: Tuple[str],
                       df_one: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Do the STL decomposition of a single grain and save the result object.

        If one of grains contains fewer then one dimensions the DataException is raised.
        :param grain: the tuple of grains.
        :type grain: tuple
        :param df_one: The TimeSeriesDataFrame with one grain.
        :type df_one: TimeSeriesDataFrame
        :returns: The data frame with season and trend columns.
        :rtype: TimeSeriesDataFrame
        :raises: DataException

        """
        self._first_observation_dates[grain] = df_one.time_index.min()
        self._last_observation_dates[grain] = df_one.time_index.max()
        if df_one.shape[0] < 2:
            raise DataException(
                'Grain {} is degenerate time series of exactly one datapoint.'.format(grain))
        series_vals = df_one[df_one.ts_value_colname].values
        stl_result = seasonal_decompose(series_vals,
                                        model=self._model_type,
                                        freq=self.seasonality,
                                        two_sided=False)
        self._stls[grain] = stl_result
        # Remove the leading nan.
        non_nan_trend = stl_result.trend[~np.isnan(stl_result.trend)]
        self._es_models[grain] = self._get_trend_model(non_nan_trend)
        return self._assign_trend_season(
            df_one, stl_result.seasonal, stl_result.trend)

    def _fit_transform_one_grain(self,
                                 grain: Tuple[str],
                                 df_one: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Infer the seasonality and trend for single grain.

        In this case we assume that fit data are the same as train data.
        This method is used in the fit_transform.
        :param grain: the tuple of grains.
        :type grain: tuple
        :param df_one: The TimeSeriesDataFrame with one grain.
        :type df_one: TimeSeriesDataFrame
        :returns: The data frame with season and trend columns.
        :rtype: TimeSeriesDataFrame
        """
        stl_result = self._stls[grain]
        return self._assign_trend_season(
            df_one, stl_result.seasonal, stl_result.trend)

    def _transform_one_grain(self,
                             grain: Tuple[str],
                             df_one: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Infer the seasonality and trend for single grain.

        :param grain: the tuple of grains.
        :type grain: tuple
        :param df_one: The TimeSeriesDataFrame with one grain.
        :type df_one: TimeSeriesDataFrame
        :returns: The data frame with season and trend columns.
        :rtype: TimeSeriesDataFrame
        """
        tsdf_freq = df_one.infer_freq()
        # Define which part of data is in training and which in testing set.
        # The data already present in training set. We know the trend for them.
        df_one_train = None  # type: Optional[TimeSeriesDataFrame]
        # The new data, we need to forecast trend.
        df_one_pred = None  # type: Optional[TimeSeriesDataFrame]
        # Split the data on training and prediction part.
        if df_one.time_index.min() < self._last_observation_dates[grain]:
            df_one_train = df_one[:self._last_observation_dates[grain]]
        if df_one.time_index.max() > self._last_observation_dates[grain]:
            df_one_pred = df_one[self._last_observation_dates[grain] + to_offset(tsdf_freq):]

        stl_result = self._stls[grain]
        if df_one_train is not None:
            offset = len(
                pd.date_range(
                    self._first_observation_dates[grain],
                    df_one.time_index.min(),
                    freq=tsdf_freq)) - 1
            end = df_one_train.shape[0] + offset
            df_one_train = self._assign_trend_season(df_one_train,
                                                     stl_result.seasonal[offset:end],
                                                     stl_result.trend[offset:end])

        if df_one_pred is not None:
            model = self._es_models[grain]
            ts_value = cast(str, self._ts_value)
            season_name = ts_value + TimeSeriesInternal.STL_SEASON_SUFFIX
            trend_name = ts_value + TimeSeriesInternal.STL_TREND_SUFFIX
            try:
                horizon = get_period_offsets_from_dates(
                    self._last_observation_dates[grain],
                    df_one_pred.time_index,
                    tsdf_freq).max()
            except KeyError:
                raise DataException('Unable to determine horizon for grain {}'.format(grain))

            fcast_start = self._last_observation_dates[grain] + self._freq
            fcast_dates = pd.date_range(start=fcast_start,
                                        periods=horizon,
                                        freq=self._freq)
            # Generate seasons for all the time periods beginning from the one next to last
            # date in the training set.
            start_season = len(pd.date_range(start=self._first_observation_dates[grain],
                                             end=self._last_observation_dates[grain],
                                             freq=self._freq)) % self.seasonality
            seasonal = [stl_result.seasonal[start_season + season % self.seasonality]
                        for season in range(len(fcast_dates))]

            if model is not None:
                point_fcast = model.forecast(steps=horizon)
            else:
                point_fcast = np.repeat(np.NaN, horizon)
            # Construct the time axis that aligns with the forecasts
            forecast_dict = {
                df_one_pred.time_colname: fcast_dates,
                trend_name: point_fcast,
                season_name: seasonal}
            if df_one_pred.grain_colnames:
                forecast_dict.update(grain_level_to_dict(df_one_pred.grain_colnames,
                                                         grain))
            # Merge the data sets and consequently, trim the unused periods.
            tsdf_temp = TimeSeriesDataFrame(forecast_dict,
                                            time_colname=df_one_pred.time_colname,
                                            grain_colnames=df_one_pred.grain_colnames)
            df_one_pred = df_one_pred.merge(tsdf_temp, left_index=True, right_index=True)
        if df_one_pred is None:
            # In this case df_one_train have to be not None.
            # This means fit_transform was called.
            return cast(TimeSeriesDataFrame, df_one_train)
        if df_one_train is None:
            # In this case df_one_pred have to be not None.
            return df_one_pred
        return cast(TimeSeriesDataFrame, pd.concat([df_one_train, df_one_pred]))

    def _assign_trend_season(self,
                             tsdf: TimeSeriesDataFrame,
                             ar_season: np.ndarray,
                             ar_trend: np.ndarray) -> TimeSeriesDataFrame:
        """
        Create the season and trend columns in the data frame.

        :param tsdf: Target data frame.
        :type tsdf: :class:`TimeSeriesDataFrame`
        :param ar_season: seasonality component.
        :type ar_season: np.ndarray
        :param ar_trend: trend component.
        :type ar_trend: np.ndarray
        :returns: The time series data frame with trend and seasonality components.
        :rtype: TimeSeriesDataFrame
        :raises: DataException

        """
        if self._ts_value is None:
            # This exception should not be raised here,
            # but enforcement of type checking requires Optopnal[str] to be
            # checked for None.
            raise DataException("Fit not called")
        season_name, trend_name = self._get_column_names(self._ts_value)

        assign_dict = {season_name: ar_season,
                       trend_name: ar_trend}
        return cast(TimeSeriesDataFrame, tsdf.assign(**assign_dict))

    def _get_column_names(self, target: str) -> Tuple[str, str]:
        """
        Return the names of columns to be generated.

        :param tsdf: The time series data frame to generate seasonality and trend for.
        :type tsdf: TimeSeriesDataFrame
        :returns: The tuple of seasonality and trend columns.
        :rtype: tuple

        """
        return (target + TimeSeriesInternal.STL_SEASON_SUFFIX,
                target + TimeSeriesInternal.STL_TREND_SUFFIX)

    @property
    def seasonality(self) -> int:
        """
        Return the number of periods after which the series values tend to repeat.

        :returns: seasonality.
        :rtype: int

        """
        return self._seasonality

    def _get_trend_model(self,
                         series_values: np.ndarray) -> 'HoltWintersResultsWrapper':
        """
        Train the Exponential Smoothing model on single series.

        This model will be used for the trend forecasting.
        :param series_values: The series with target values.
        :type series_values: np.ndarray
        :returns: The Exponential smoothing model .
        :rtype: HoltWintersResultsWrapper

        """
        # Model type consistency checks
        self._assert_damping_valid()
        self._assert_mult_model_valid(series_values)

        # Make sure the series is long enough for fitting
        # If not, impute values to "complete" the series
        series_values = _complete_short_series(series_values, 1)

        # Internal function for fitting a statsmodel ETS model
        #  and determining if a model type should be considered in selection
        # ------------------------------------------------------------------
        def fit_sm(model_type):
            trend_type, seas_type, damped = model_type

            if self._sm9_bug_workaround:
                series_values_safe = \
                    _extend_series_for_sm9_bug(series_values, 1,
                                               model_type)
            else:
                series_values_safe = series_values

            ets_model = \
                ExponentialSmoothing(series_values_safe,
                                     trend=self._char_to_statsmodels_opt[trend_type],
                                     seasonal=self._char_to_statsmodels_opt[seas_type],
                                     damped=damped,
                                     seasonal_periods=None)

            return ets_model.fit(use_boxcox=self.use_boxcox,
                                 use_basinhopping=self.use_basinhopping)

        def model_is_valid(model_type, has_zero_or_neg):
            trend_type, seas_type, damped = model_type

            if trend_type == 'N' and damped:
                return False

            if (trend_type == 'M' or seas_type == 'M') \
                    and has_zero_or_neg:
                return False

            return True
        # ------------------------------------------------------------------

        # Make a grid of model types and select the one with minimum loss
        has_zero_or_neg = (series_values <= 0.0).any()
        type_grid = self._make_param_grid(False)
        fit_models = {mtype: fit_sm(mtype) for mtype in type_grid
                      if model_is_valid(mtype, has_zero_or_neg)}
        best_type, best_result = \
            min(fit_models.items(),
                key=lambda it: getattr(it[1], self.selection_metric))

        return best_result

    def _assert_damping_valid(self) -> None:
        """
        Make sure the damped setting is consistent with the model type setting.

        :raises: ConfigException

        """
        if self._get_two_letter_model_type()[0] == 'N' and self.damped:
            raise ConfigException(
                ('Inconsistent settings: `model_type`={0} and `damped`={1}. ' +
                 'Damping can only be applied when there is a trend term.')
                .format(self._model_type, self.damped))

    def _assert_mult_model_valid(self, series_values: pd.Series) -> None:
        """
        Make sure that multiplicative model settings are consistent.

        Currently, the underlying fit cannot handle zero or negative valued
        series with multiplicative models.

        :param series_values: The series with the values.
        :type series_values: pd.Series
        :raises: ConfigException

        """
        if 'M' in self._get_two_letter_model_type() and (series_values <= 0.0).any():
            raise ConfigException(
                ('Cannot use multiplicative model type {0} because trend ' +
                 'contains negative or zero values.')
                .format(self._model_type))

    def _make_param_grid(self, is_seasonal: bool) -> Iterator[Tuple[str, str, bool]]:
        """
        Make an iterable of model type triples (trend, seasonal, damping).

        :param is_seasonal: Does model include seasonality?
        :type is_seasonal: bool
        :returns: The model grid to be fitted for the best model selection.
        :rtype: list

        """
        mtype = self._get_two_letter_model_type()
        trend_in, seas_in = mtype
        trend_grid = [trend_in] if trend_in != 'Z' else ['A', 'M', 'N']

        if is_seasonal:
            seasonal_grid = [seas_in] if seas_in != 'Z' else ['A', 'M', 'N']
        else:
            seasonal_grid = ['N']

        damped_grid = [self.damped] \
            if self.damped is not None else [True, False]

        return product(trend_grid, seasonal_grid, damped_grid)

    def _get_two_letter_model_type(self) -> str:
        """
        Return two letter code of model. We currently support only AA and MM.

        :returns: The two letter code of a model.
                  The first letter is trend type (multiplicative/additive),
                  the second letter is a seasonality type.
        :rtype: str

        """
        return 'AA' if self._model_type == 'additive' else 'MM'

    def _apply_func_to_grains(self,
                              func: 'Callable[[Tuple[str], TimeSeriesDataFrame], TimeSeriesDataFrame]',
                              data_frame: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Apply function func to all grains of the data_frame and concatenate their output to another TSDF.

        :param data_frame: The initial data frame.
        :type data_frame: TimeSeriesDataFrame
        :param func: the function, returning TimeSeriesDataFrame and taking grain tuple and
                     TimeSeriesDataFrame as a parameters.
        :type func: function
        :param data_frame: target time series data frame.
        :type data_frame: TimeSeriesDataFrame
        :returns: The modified data frame.
        :rtype: TimeSeriesDataFrame

        """
        result = []
        for grain, X in data_frame.groupby_grain():
            result.append(func(grain, X))
        result_df = pd.concat(result)
        result_df.sort_index(inplace=True)
        return cast(TimeSeriesDataFrame, result_df)
