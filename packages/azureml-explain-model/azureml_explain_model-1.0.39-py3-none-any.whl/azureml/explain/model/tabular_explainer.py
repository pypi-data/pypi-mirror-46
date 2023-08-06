# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

from .common.base_explainer import BaseExplainer
from .common.structured_model_explainer import PureStructuredModelExplainer
from .dataset.dataset_wrapper import DatasetWrapper
from .dataset.decorator import tabular_decorator, add_transformations_to_init, add_transformations_to_explain
from .explanation.explanation import _create_raw_feats_global_explanation, _create_raw_feats_local_explanation, \
    _get_raw_explainer_create_explanation_kwargs
from azureml.explain.model._internal.constants import ExplainParams
from .shap.tree_explainer import TreeExplainer
from .shap.deep_explainer import DeepExplainer
from .shap.kernel_explainer import KernelExplainer

InvalidExplainerErr = 'Could not find valid explainer to explain model'


class TabularExplainer(BaseExplainer):
    """Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

    @add_transformations_to_init
    def __init__(self, model, initialization_examples, explain_subset=None, features=None, classes=None,
                 transformations=None, **kwargs):
        """Initialize the TabularExplainer.

        :param model: The model or pipeline to explain.
        :type model: model that implements predict or predict_proba or pipeline function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation, which will speed up the explanation
            process when number of features is large and the user already knows the set of interested
            features. The subset can be the top-k features from the model summary. This argument is not supported when
            transformations are set.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param transformations: List of tuples describing the column name and transformer. When transformations are
        provided, explanations are of the features before the transformation. The format for
        transformations is same as the one here: https://github.com/scikit-learn-contrib/sklearn-pandas.
        If the user is using a transformation that is not in the list of sklearn.preprocessing transformations that
        we support then we cannot take a list of more than one column as input for the transformation.
        A user can use the following sklearn.preprocessing  transformations with a list of columns since these are
        already one to many or one to one: Binarizer, KBinsDiscretizer, KernelCenterer, LabelEncoder, MaxAbsScaler,
        MinMaxScaler, Normalizer, OneHotEncoder, OrdinalEncoder, PowerTransformer, QuantileTransformer, RobustScaler,
        StandardScaler.
        Examples for transformations that work:
        [
            (["col1", "col2"], sklearn_one_hot_encoder),
            (["col3"], None) #col3 passes as is
        ]
        [
            (["col1"], my_own_transformer),
            (["col2"], my_own_transformer),
        ]
        Example of transformations that would raise an error since it cannot be interpreted as one to many:
        [
            (["col1", "col2"], my_own_transformer)
        ]
        This would not work since it is hard to make out whether my_own_transformer gives a many to many or one to many
        mapping when taking a sequence of columns.
        :type transformations: list[tuple]
        """
        super(TabularExplainer, self).__init__(**kwargs)
        self._logger.debug('Initializing TabularExplainer')

        if transformations is not None and explain_subset is not None:
            raise ValueError("explain_subset not supported with non-None transformations")

        self.model = model
        self.features = features
        self.classes = classes
        self.explain_subset = explain_subset
        kwargs[ExplainParams.EXPLAIN_SUBSET] = self.explain_subset
        kwargs[ExplainParams.FEATURES] = features
        kwargs[ExplainParams.CLASSES] = classes
        if not isinstance(initialization_examples, DatasetWrapper):
            self._logger.debug('Wrapping init examples with DatasetWrapper')
            self.initialization_examples = DatasetWrapper(initialization_examples)
        else:
            self.initialization_examples = initialization_examples
        uninitialized_explainers = self._get_uninitialized_explainers()
        is_valid = False
        for uninitialized_explainer in uninitialized_explainers:
            try:
                if issubclass(uninitialized_explainer, PureStructuredModelExplainer):
                    self.explainer = uninitialized_explainer(self.model, **kwargs)
                else:
                    self.explainer = uninitialized_explainer(self.model, self.initialization_examples, **kwargs)
                self.explainer._datamapper = self._datamapper
                self._logger.info('Initialized valid explainer {} with args {}'.format(self.explainer, kwargs))
                is_valid = True
                break
            except Exception as ex:
                self._logger.info('Failed to initialize explainer {} due to error: {}'
                                  .format(uninitialized_explainer, ex))
        if not is_valid:
            self._logger.info(InvalidExplainerErr)
            raise ValueError(InvalidExplainerErr)

    def _get_uninitialized_explainers(self):
        """Return the uninitialized explainers used by the tabular explainer.

        :return: A list of the uninitialized explainers.
        :rtype: list
        """
        return [TreeExplainer, DeepExplainer, KernelExplainer]

    @add_transformations_to_explain
    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None, include_local=True):
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
        kwargs = {ExplainParams.SAMPLING_POLICY: sampling_policy, ExplainParams.INCLUDE_LOCAL: include_local}
        explanation = self.explainer.explain_global(evaluation_examples, **kwargs)

        # if transformations have been passed, return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(explanation=explanation)

        return explanation if self._datamapper is None else _create_raw_feats_global_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)

    @add_transformations_to_explain
    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Locally explains the black box model or function.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation. If SHAP is used for the
            explanation, it will also have the properties of the ExpectedValuesMixin. If the model does
            classification, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        explanation = self.explainer.explain_local(evaluation_examples)

        # if transformations have been passed, then return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(explanation=explanation)

        return explanation if self._datamapper is None else _create_raw_feats_local_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)
