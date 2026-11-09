"""Strategy pattern: interchangeable evaluation metrics."""

from abc import ABC, abstractmethod
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class MetricStrategy(ABC):
    """Common interface for all metric strategies."""

    name: str

    @abstractmethod
    def calculate(self, y_true, y_pred) -> float:
        raise NotImplementedError


class AccuracyMetric(MetricStrategy):
    name = "accuracy"

    def calculate(self, y_true, y_pred) -> float:
        return float(accuracy_score(y_true, y_pred))


class F1Metric(MetricStrategy):
    name = "f1"

    def __init__(self, average: str = "weighted"):
        self.average = average

    def calculate(self, y_true, y_pred) -> float:
        return float(f1_score(y_true, y_pred, average=self.average, zero_division=0))


class PrecisionMetric(MetricStrategy):
    name = "precision"

    def __init__(self, average: str = "weighted"):
        self.average = average

    def calculate(self, y_true, y_pred) -> float:
        return float(precision_score(
            y_true, y_pred, average=self.average, zero_division=0
        ))


class RecallMetric(MetricStrategy):
    name = "recall"

    def __init__(self, average: str = "weighted"):
        self.average = average

    def calculate(self, y_true, y_pred) -> float:
        return float(recall_score(
            y_true, y_pred, average=self.average, zero_division=0
        ))


def calculate_metrics(y_true, y_pred, strategies):
    """Evaluate predictions using the supplied strategy objects."""
    if not strategies:
        raise ValueError("At least one metric strategy must be supplied.")
    return {strategy.name: strategy.calculate(y_true, y_pred)
            for strategy in strategies}
