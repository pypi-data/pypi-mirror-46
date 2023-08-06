# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the TreeExplainer for returning explanations for tree-based models."""

from azureml.explain.model.shap import tree_explainer
from azureml.explain.model.dataset.decorator import tabular_decorator
from ..scoring.scoring_explainer import TreeScoringExplainer
from azureml.explain.model._internal.constants import ExplainType
from ..explanation.explanation import _create_local_explanation
from .kwargs_utils import _get_explain_global_kwargs
from ..common.aggregate import contrib_aggregator


@contrib_aggregator
class TreeExplainer(tree_explainer.TreeExplainer):
    """Defines the TreeExplainer for returning explanations for tree-based models."""

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
        kwargs = _get_explain_global_kwargs(sampling_policy, ExplainType.SHAP_TREE, include_local)
        return self._explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the model by using shap's tree explainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: DatasetWrapper
        :return: A model explanation object. It is guaranteed to be a LocalExplanation which also has the properties
            of ExpectedValuesMixin. If the model is a classfier, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = super(TreeExplainer, self)._get_explain_local_kwargs(evaluation_examples)
        return _create_local_explanation(**kwargs)

    def create_scoring_explainer(self, data_transformer=None):
        """Create the scoring explainer for the tree explainer.

        :param data_transformer: An object that converts raw features to engineered via .transform().
            The data output by transform should mirror the data passed into explain_global.
        :type data_transformer: An object with .transform()
        :return: The scoring explainer based on the model being explained.
        :rtype: TreeScoringExplainer
        """
        return TreeScoringExplainer(self.model, data_transformer=data_transformer, data_mapper=self._datamapper)
