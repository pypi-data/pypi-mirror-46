# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Generic bag of words transformer."""
from typing import Tuple, Optional, Union

import logging

import numpy as np
import pandas as pd
from sklearn.pipeline import make_union, make_pipeline, Pipeline, FeatureUnion
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import RobustScaler

from ..automltransformer import AutoMLTransformer
from .stringcast_transformer import StringCastTransformer
from .stats_transformer import StatsTransformer
from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.types import DataSingleColumnInputType, DataInputType


class BagOfWordsTransformer(AutoMLTransformer):
    """Generic bag of words transformer."""

    def __init__(self, logger: Optional[logging.Logger] = None, max_wordgrams: int = int(2e5),
                 wordgram_range: Tuple[int, int] = (1, 2),
                 chargram_range: Tuple[int, int] = (3, 3), norm: str = "l2", max_df: float = 1.0,
                 include_dense_features: bool = False, use_idf: bool = False) -> None:
        """Create the bag of words transformer."""
        super().__init__()
        self._init_logger(logger)
        self._max_wordgrams = max_wordgrams
        self._wordgram_range = wordgram_range
        self._chargram_range = chargram_range
        self._include_dense_features = include_dense_features
        self._norm = norm
        self._max_df = max_df
        self._pipelines = None                  # type: Optional[Union[Pipeline, FeatureUnion]]
        self._use_idf = use_idf

    @function_debug_log_wrapped
    def fit(self, X: DataInputType, y: DataSingleColumnInputType) -> "BagOfWordsTransformer":
        """
        Fit the current model to given input data.

        :param X: Input data.
        :param y: Input labels.
        :return: The object itself.
        """
        pipeline_list = []

        if self._include_dense_features:
            pipeline_list.append(make_pipeline(StatsTransformer(),
                                               DictVectorizer(),
                                               RobustScaler(with_centering=False)))

        if self._chargram_range != (0, 0):
            pipeline_list.append(TfidfVectorizer(use_idf=self._use_idf,
                                                 dtype=np.float32,
                                                 analyzer="char",
                                                 norm=self._norm,
                                                 max_df=self._max_df,
                                                 ngram_range=self._chargram_range))

        if self._wordgram_range != (0, 0):
            pipeline_list.append(TfidfVectorizer(use_idf=self._use_idf,
                                                 dtype=np.float32,
                                                 max_features=self._max_wordgrams,
                                                 analyzer="word",
                                                 ngram_range=self._wordgram_range))

        if pipeline_list:
            self._pipelines = make_union(*pipeline_list)
            self._pipelines.fit(X)
        return self

    @function_debug_log_wrapped
    def transform(self, X: DataInputType) -> DataInputType:
        """Transform the given data.

        :param X: Input data.
        :return: Transformed data.
        """
        if self._pipelines:
            features = self._pipelines.transform(X)
            return features
        else:
            return np.array([])
