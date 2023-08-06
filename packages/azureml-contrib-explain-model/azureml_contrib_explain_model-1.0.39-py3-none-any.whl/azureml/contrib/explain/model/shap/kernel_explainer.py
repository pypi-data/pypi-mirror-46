# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the KernelExplainer for computing explanations on black box models or functions."""

from azureml.explain.model.shap import kernel_explainer
from azureml.explain.model.dataset.decorator import tabular_decorator, init_tabular_decorator
from azureml.explain.model._internal.constants import Defaults, ExplainType
from azureml.explain.model.common.blackbox_explainer import init_blackbox_decorator
from ..scoring.scoring_explainer import KNNScoringExplainer
from ..explanation.explanation import _create_local_explanation
from azureml.explain.model.common.explanation_utils import _transform_data
from .kwargs_utils import _get_explain_global_kwargs
from ..common.aggregate import contrib_aggregator


@contrib_aggregator
class KernelExplainer(kernel_explainer.KernelExplainer):
    """Defines the Kernel Explainer for explaining black box models or functions."""

    @init_tabular_decorator
    @init_blackbox_decorator
    def __init__(self, model, initialization_examples, is_function=False, explain_subset=None,
                 nsamples=Defaults.AUTO, features=None, classes=None, nclusters=10,
                 show_progress=True, **kwargs):
        """Initialize the KernelExplainer.

        :param model: The model to explain or function if is_function is True.
        :type model: model that implements predict or predict_proba or function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param is_function: Default set to false, set to True if passing function instead of model.
        :type is_function: bool
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation, which will speed up the explanation
            process when number of features is large and the user already knows the set of interested
            features. The subset can be the top-k features from the model summary.
        :type explain_subset: list[int]
        :param nsamples: Default to 'auto'. Number of times to re-evaluate the model when
            explaining each prediction. More samples lead to lower variance estimates of the
            feature importance values, but incur more computation cost. When 'auto' is provided,
            the number of samples is computed according to a heuristic rule.
        :type nsamples: 'auto' or int
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param nclusters: Number of means to use for approximation. A dataset is summarized with nclusters mean
            samples weighted by the number of data points they each represent. When the number of initialization
            examples is larger than (10 x nclusters), those examples will be summarized with k-means where
            k = nclusters.
        :type nclusters: int
        :param show_progress: Default to 'True'.  Determines whether to display the explanation status bar
            when using shap_values from the KernelExplainer.
        :type show_progress: bool
        """
        super(KernelExplainer, self).__init__(model, initialization_examples, is_function=is_function,
                                              explain_subset=explain_subset, nsamples=nsamples, features=features,
                                              classes=classes, nclusters=nclusters, show_progress=show_progress,
                                              **kwargs)
        self._logger.debug('Initializing KernelExplainer')

    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None,
                       include_local=True):
        """Explain the model globally by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param include_local: Include the local explanations in the returned global explanation.
            If include_local is False, will stream the local explanations to aggregate to global.
        :type include_local: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation which also has the properties
            of LocalExplanation and ExpectedValuesMixin. If the model is a classifier, it will have the properties of
            PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = _get_explain_global_kwargs(sampling_policy, ExplainType.SHAP_KERNEL, include_local)
        return self._explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the function locally by using SHAP's KernelExplainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: DatasetWrapper
        :return: A model explanation object. It is guaranteed to be a LocalExplanation which also has the properties
            of ExpectedValuesMixin. If the model is a classfier, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        if self._column_indexer:
            evaluation_examples.apply_indexer(self._column_indexer)

        kwargs = super(KernelExplainer, self)._get_explain_local_kwargs(evaluation_examples)
        return _create_local_explanation(**kwargs)

    def create_scoring_explainer(self, evaluation_examples, data_transformer=None):
        """Create the scoring explainer for the kernel explainer.

        This will run explain_global in the background.

        :param evaluation_examples: The evaluation samples that have been used to generate
            the local importance values.
        :type evaluation_examples: numpy.array or iml.datatypes.DenseData or scipy.sparse.csr_matrix
        :param data_transformer: An object that converts raw features to engineered via .transform().
            The data output by transform should mirror the data passed into explain_global.
        :type data_transformer: An object with .transform()
        :return: The scoring explainer based on the model being explained.
        :rtype: KNNScoringExplainer
        """
        # convert raw data to engineered before doing a global explanation
        evaluation_data = _transform_data(evaluation_examples, data_mapper=self._datamapper,
                                          data_transformer=data_transformer)

        explanation = self.explain_global(evaluation_data)
        return KNNScoringExplainer(evaluation_data,
                                   explanation.local_importance_values,
                                   data_transformer=data_transformer,
                                   data_mapper=self._datamapper)
