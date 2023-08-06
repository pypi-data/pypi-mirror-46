# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines a decorator for tabular data which wraps pandas dataframes, scipy and numpy arrays in a DatasetWrapper."""

from .dataset_wrapper import DatasetWrapper
from azureml.explain.model._internal.raw_explain import DataMapper
from azureml.explain.model._internal.constants import ExplainerArgs

from functools import wraps


def tabular_decorator(explain_func):
    """Decorate an explanation function to wrap evaluation examples in a DatasetWrapper.

    :param explain_func: An explanation function where the first argument is a dataset.
    :type explain_func: explanation function
    """
    @wraps(explain_func)
    def explain_func_wrapper(self, evaluation_examples, **kwargs):
        if not isinstance(evaluation_examples, DatasetWrapper):
            self._logger.debug('Eval examples not wrapped, wrapping')
            evaluation_examples = DatasetWrapper(evaluation_examples)
        return explain_func(self, evaluation_examples, **kwargs)
    return explain_func_wrapper


def init_tabular_decorator(init_func):
    """Decorate a constructor to wrap initialization examples in a DatasetWrapper.

    Provided for convenience for tabular data explainers.

    :param init_func: Initialization constructor where the second argument is a dataset.
    :type init_func: Initialization constructor.
    """
    @wraps(init_func)
    def init_wrapper(self, model, initialization_examples, *args, **kwargs):
        if not isinstance(initialization_examples, DatasetWrapper):
            initialization_examples = DatasetWrapper(initialization_examples)
        return init_func(self, model, initialization_examples, *args, **kwargs)
    return init_wrapper


def _transform(obj, x):
    """Transform the input using the _datamapper field in obj.

    :param obj: explainer object
    :type obj: class that implements BaseExplainer
    :param x: input data
    :type x: numpy array or pandas DataFrame
    :return: transformed data
    :rtype: numpy.array or scipy.sparse matrix
    """
    return x if obj._datamapper is None else obj._datamapper.transform(x)


def add_transformations_to_explain(explain_func):
    """Decorate explain_global or explain_local so that transformations to input data are done before calling explain.

    :param explain_func: explain_global or explain_local in a class that implements BaseExplainer
    :type explain_func: function
    """
    @wraps(explain_func)
    def transform_data_wrapper(self, evaluation_examples, **kwargs):
        evaluation_examples = _transform(self, evaluation_examples)
        return explain_func(self, evaluation_examples, **kwargs)

    return transform_data_wrapper


def add_transformations_to_init(init_func):
    """Decorate the constructor so that transformations are done before calling the constructor.

    :param init_func: constructor for an explainer
    :type init_func: function
    """
    @wraps(init_func)
    def transform_data_wrapper(self, model, initialization_examples, *args, **kwargs):
        if kwargs.get(ExplainerArgs.TRANSFORMATIONS) is not None:
            self._datamapper = DataMapper(kwargs[ExplainerArgs.TRANSFORMATIONS])
            initialization_examples = self._datamapper.transform(initialization_examples)
        else:
            self._datamapper = None

        return init_func(self, model, initialization_examples, *args, **kwargs)

    return transform_data_wrapper
