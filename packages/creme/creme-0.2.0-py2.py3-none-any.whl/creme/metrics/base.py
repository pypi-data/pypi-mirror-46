import abc
import typing

from .. import base


__all__ = [
    'BinaryClassificationMetric',
    'MultiClassificationMetric',
    'RegressionMetric'
]


Label = typing.Union[bool, str, int]
Proba = float


class BaseMetric(abc.ABC):

    @abc.abstractmethod
    def get(self) -> float:
        """Returns the current value of the metric."""

    @abc.abstractmethod
    def works_with(self, model) -> bool:
        """Tells if a metric can work with a given model or not."""

    @property
    @abc.abstractmethod
    def bigger_is_better(self) -> bool:
        """Indicates if a high value is better than a low one or not."""

    def __str__(self):
        """Returns the class name along with the current value of the metric."""
        return f'{self.__class__.__name__}: {self.get():.6f}'.rstrip('0')

    def __repr__(self):
        return str(self)


class ClassificationMetric(BaseMetric):

    @property
    @abc.abstractmethod
    def requires_labels(self):
        """Helps to indicate if labels are required instead of probabilities."""


class BinaryClassificationMetric(ClassificationMetric):

    @abc.abstractmethod
    def update(self, y_true: bool, y_pred: typing.Union[bool, typing.Dict[Label, Proba]]):
        """Updates the metric."""

    def works_with(self, model):
        return isinstance(model, base.BinaryClassifier)


class MultiClassificationMetric(BinaryClassificationMetric):

    @abc.abstractmethod
    def update(self, y_true: Label, y_pred: typing.Union[Label, typing.Dict[Label, Proba]]):
        """Updates the metric."""

    def works_with(self, model):
        return isinstance(model, (base.BinaryClassifier, base.MultiClassifier))


class RegressionMetric(BaseMetric):

    @abc.abstractmethod
    def update(self, y_true: float, y_pred: float):
        """Updates the metric."""

    def works_with(self, model):
        return isinstance(model, base.Regressor)
