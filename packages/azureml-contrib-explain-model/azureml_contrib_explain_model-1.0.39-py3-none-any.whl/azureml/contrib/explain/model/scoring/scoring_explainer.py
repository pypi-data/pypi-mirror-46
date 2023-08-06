# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines scoring models for approximating feature importance values."""

import scipy as sp
import numpy as np
import logging
import os
from abc import ABCMeta, abstractmethod
from sklearn.externals import joblib

try:
    from azureml._logging import ChainedIdentity
except ImportError:
    from azureml.explain.model.common.chained_identity import ChainedIdentity

from azureml.explain.model._internal.constants import SKLearn, LoggingNamespace
from azureml.explain.model.common.explanation_utils import _get_raw_feature_importances, _get_dense_examples, \
    _transform_data

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap

LOGGER = '_logger'


class ScoringExplainer(ChainedIdentity):
    """Defines a scoring model."""

    __metaclass__ = ABCMeta

    def __init__(self, data_transformer=None, data_mapper=None, **kwargs):
        """Initialize the ScoringExplainer.

        :param data_transformer: The pipeline of transformations that should be run on the data
            before explanation. If None, no transformations will be done.
        :type data_transformer: An object implementing .transform()
        :param data_mapper: A DataMapper object with a feature map and .transform()
        :type data_mapper: DataMapper
        """
        super(ScoringExplainer, self).__init__(**kwargs)
        self._logger.debug('Initializing ScoringExplainer')
        if data_transformer is not None and data_mapper is not None:
            raise Exception('Only one of data_transformer or data_mapper should be passed.')
        self._data_transformer = data_transformer
        self._data_mapper = data_mapper

    @abstractmethod
    def explain(self, evaluation_examples):
        """Use the model for scoring to approximate the feature importance values of data."""
        pass

    def _get_raw_explanations(self, engineered_importances):
        """Convert from an explanation of engineered features to an explanation of raw features.

        :param engineered_importances: The results of calling .explain() on engineered data.
        :type engineered_importances: np.array
        :return: The importances for the raw features originally passed to the scoring explainer.
        :rtype: np.array
        """
        if self._data_mapper is None:
            raise Exception('Feature map must be passed in to calculate raw feature importances.')
        return _get_raw_feature_importances(engineered_importances, self._data_mapper.feature_map)

    def predict(self, evaluation_examples):
        """Use the TreeExplainer and tree model for scoring to get the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype: list
        """
        return self.explain(evaluation_examples)

    def save(self, name, directory='.'):
        """Save the scoring model to disk.

        :param name: The filename under which the pickled scoring model should be stored.
        :type name: str
        :param directory: The directory under which the pickle file should be stored.
            If it doesn't exist, it will be created.
        :type directory: str
        :return: The path used.
        :rtype: str
        """
        os.makedirs(directory, exist_ok=True)
        location = os.path.join(directory, name)
        with open(location, 'wb') as stream:
            joblib.dump(self, stream)
        return location

    @staticmethod
    def load(path):
        """Load the scoring model from disk.

        :param path: The path under which the pickled scoring model was stored.
        :type path: str
        :return: The scoring model from an explanation, loaded from disk.
        :rtype: azureml.contrib.explain.model.scoring.scoring_explainer.ScoringExplainer
        """
        with open(path, 'rb') as stream:
            scoring_explainer = joblib.load(stream)
        return scoring_explainer


class TreeScoringExplainer(ScoringExplainer):
    """Defines a scoring model based on TreeExplainer."""

    def __init__(self, tree_model, data_transformer=None, data_mapper=None, **kwargs):
        """Initialize the TreeScoringExplainer.

        :param tree_model: The tree model to build the TreeExplainer from for local explanations.
        :type tree_model: tree-based model
        :param data_transformer: The pipeline of transformations that should be run on the data
            before explanation. If None, no transformations will be done.
        :type data_transformer: An object implementing .transform()
        :param data_mapper: A DataMapper object with a feature map and .transform()
        :type data_mapper: DataMapper
        """
        super(TreeScoringExplainer, self).__init__(data_transformer=data_transformer,
                                                   data_mapper=data_mapper,
                                                   **kwargs)
        self._logger.debug('Initializing TreeScoringExplainer')
        self.tree_explainer = shap.TreeExplainer(tree_model)
        # Only lightgbm and xgboost models don't directly fail with sparse data currently
        model_type_str = str(type(tree_model))
        self._convert_to_dense = not ("xgboost" in model_type_str or "lightgbm" in model_type_str)

    def explain(self, evaluation_examples):
        """Use the TreeExplainer and tree model for scoring to get the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        if self._convert_to_dense:
            evaluation_examples = _get_dense_examples(evaluation_examples)

        # convert raw data to engineered before explaining
        data = _transform_data(evaluation_examples, data_mapper=self._data_mapper,
                               data_transformer=self._data_transformer)

        values = self.tree_explainer.shap_values(data)
        if self._data_mapper is not None:
            values = np.array(values) if isinstance(values, list) else values
            return self._get_raw_explanations(values).tolist()
        if not isinstance(values, list):
            values = values.tolist()
        return values

    def __getstate__(self):
        """Influence how TreeScoringExplainer is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how TreeScoringExplainer is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(LoggingNamespace.AZUREML)
        self._logger = parent.getChild(self._identity)


class KNNScoringExplainer(ScoringExplainer):
    """Defines a scoring model based on 1-Nearest Neighbor."""

    def __init__(self, evaluation_examples, local_importance_values, data_transformer=None, data_mapper=None,
                 **kwargs):
        """Initialize the KNNScoringExplainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param local_importance_values: The feature importance values.
        :type local_importance_values: list
        :param data_transformer: The pipeline of transformations that should be run on the data
            before explanation. If None, no transformations will be done.
        :type data_transformer: An object implementing .transform()
        :param data_mapper: A list of lists of generated feature indices for each raw feature.
        :type data_mapper: list[list[]]
        """
        super(KNNScoringExplainer, self).__init__(data_transformer=data_transformer,
                                                  data_mapper=data_mapper,
                                                  **kwargs)
        self._logger.debug('Initializing KNNScoringExplainer')
        # normalize features prior to using knn
        from sklearn.preprocessing import StandardScaler
        if sp.sparse.issparse(evaluation_examples):
            self._logger.debug('In KNNScoringExplainer for sparse data using StandardScaler without mean')
            self.scaler = StandardScaler(with_mean=False).fit(evaluation_examples)
        else:
            self._logger.debug('In KNNScoringExplainer for dense data using StandardScaler with mean')
            self.scaler = StandardScaler().fit(evaluation_examples)
        # compute nearest neighbors, can be used in scoring path
        from sklearn.neighbors import NearestNeighbors
        scaled_data = self.scaler.transform(evaluation_examples)
        self.neighbors = NearestNeighbors(n_neighbors=1, algorithm=SKLearn.BALL_TREE).fit(scaled_data)
        self.nn_feature_importance = np.array(local_importance_values)
        self.classification = len(self.nn_feature_importance.shape) == 3

    def explain(self, evaluation_examples):
        """Use the KNN model for scoring to approximate the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        data = evaluation_examples

        # convert raw data to engineered before explaining
        if self._data_mapper is not None:
            data = self._data_mapper.transform(data)
        elif self._data_transformer is not None:
            data = self._data_transformer.transform(data)

        _, indices = self.neighbors.kneighbors(self.scaler.transform(data))
        # flatten indices for 1-NN
        indices = [index for row in indices for index in row]
        if self.classification:
            values = self.nn_feature_importance[:, indices]
        else:
            values = self.nn_feature_importance[indices]
        if self._data_mapper is not None:
            return self._get_raw_explanations(values).tolist()
        if not isinstance(values, list):
            values = values.tolist()
        return values

    def __getstate__(self):
        """Influence how KNNScoringExplainer is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how KNNScoringExplainer is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(LoggingNamespace.AZUREML)
        self._logger = parent.getChild(self._identity)


class LinearScoringExplainer(ScoringExplainer):
    """Defines a scoring model based on LinearExplainer."""

    def __init__(self, linear_model, initialization_examples, data_transformer=None, data_mapper=None, **kwargs):
        """Initialize the LinearScoringExplainer.

        :param linear_model: The linear model to build the LinearExplainer from for local explanations.
        :type linear_model: linear model
        :param data_transformer: The pipeline of transformations that should be run on the data
            before explanation. If None, no transformations will be done.
        :type data_transformer: An object implementing .transform()
        :param data_mapper: A list of lists of generated feature indices for each raw feature.
        :type data_mapper: list[list[]]
        """
        super(LinearScoringExplainer, self).__init__(data_transformer=data_transformer,
                                                     data_mapper=data_mapper,
                                                     **kwargs)
        self._logger.debug('Initializing LinearScoringExplainer')
        self.linear_explainer = shap.LinearExplainer(linear_model, initialization_examples)

    def explain(self, evaluation_examples):
        """Use the LinearExplainer for scoring to get the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        data = evaluation_examples

        # convert raw data to engineered before explaining
        if self._data_mapper is not None:
            data = self._data_mapper.transform(data)
        elif self._data_transformer is not None:
            data = self._data_transformer.transform(data)

        values = self.linear_explainer.shap_values(data)
        if self._data_mapper is not None:
            return self._get_raw_explanations(values).tolist()
        if not isinstance(values, list):
            values = values.tolist()
        return values

    def __getstate__(self):
        """Influence how LinearScoringExplainer is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how LinearScoringExplainer is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(LoggingNamespace.AZUREML)
        self._logger = parent.getChild(self._identity)
