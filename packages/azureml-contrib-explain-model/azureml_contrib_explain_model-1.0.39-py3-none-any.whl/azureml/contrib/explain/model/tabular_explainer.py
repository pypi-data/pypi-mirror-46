# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

from azureml.exceptions import UserErrorException

from azureml.explain.model import tabular_explainer
from azureml.explain.model.dataset.decorator import add_transformations_to_explain, tabular_decorator
from azureml.explain.model.explanation.explanation import _create_raw_feats_global_explanation, \
    _get_raw_explainer_create_explanation_kwargs
from azureml.explain.model._internal.constants import ExplainParams
from .shap.tree_explainer import TreeExplainer
from .shap.deep_explainer import DeepExplainer
from .shap.kernel_explainer import KernelExplainer


class TabularExplainer(tabular_explainer.TabularExplainer):
    """Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

    @add_transformations_to_explain
    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None,
                       include_local=True):
        """Globally explains the black box model or function.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param include_local: Include the local explanations in the returned global explanation.
            If include_local is False, will stream the local explanations to aggregate to global.
        :type include_local: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If SHAP is used for the
            explanation, it will also have the properties of a LocalExplanation and the ExpectedValuesMixin. If the
            model does classification, it will have the properties of the PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = {ExplainParams.SAMPLING_POLICY: sampling_policy,
                  ExplainParams.INCLUDE_LOCAL: include_local}
        explanation = self.explainer.explain_global(evaluation_examples, **kwargs)

        # if transformations have been passed, return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(explanation=explanation)

        return explanation if self._datamapper is None else _create_raw_feats_global_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)

    def _get_uninitialized_explainers(self):
        """Return the uninitialized explainers used by the tabular explainer.

        :return: A list of the uninitialized explainers.
        :rtype: list
        """
        return [TreeExplainer, DeepExplainer, KernelExplainer]

    def create_scoring_explainer(self, evaluation_examples=None, data_transformer=None):
        """Create the scoring explainer for the tabular explainer.

        If the model being explained is not tree-based, evaluation_examples must be passed.

        :param evaluation_examples: The evaluation samples that have been used to generate
            the local importance values.
        :type evaluation_examples: numpy.array or iml.datatypes.DenseData or scipy.sparse.csr_matrix
        :param data_transformer: An object that converts raw features to engineered via .transform().
            The data output by transform should mirror the data passed into explain_global.
        :type data_transformer: An object with .transform()
        :return: The scoring explainer based on the model being explained.
        :rtype: ScoringExplainer
        """
        if self._datamapper is not None and data_transformer is not None:
            raise UserErrorException('If transformations for raw feature explanation '
                                     'were passed into the TabularExplainer init, '
                                     'please do not use data_transformer here.')
        if isinstance(self.explainer, TreeExplainer):
            return self.explainer.create_scoring_explainer(data_transformer=data_transformer)
        else:
            if evaluation_examples is None:
                raise Exception('For this type of model, '
                                'please provide evaluation examples to create_scoring_explainer.')
            return self.explainer.create_scoring_explainer(evaluation_examples,
                                                           data_transformer=data_transformer)
