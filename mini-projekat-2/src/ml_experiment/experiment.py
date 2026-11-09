"""Template Method pattern: fixed experiment workflow with customisable steps."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from .decorators import measure_time
from .metrics import AccuracyMetric, F1Metric, calculate_metrics
from .models import ModelFactory
from .observers import EventPublisher, TrainingEvent


@dataclass
class ExperimentResult:
    model_name: str
    metrics: dict[str, float]
    duration_seconds: float
    predictions: Any


class BaseExperiment(ABC):
    """Defines the invariant run sequence; subclasses provide configuration."""

    def __init__(self, publisher=None):
        self.publisher = publisher or EventPublisher()
        self.last_duration_seconds = 0.0

    def run(self) -> ExperimentResult:
        self.publisher.publish(TrainingEvent("started", "Experiment started"))
        try:
            X, y = self.load_data()
            X_train, X_test, y_train, y_test = self.split_data(X, y)
            model = self.create_model()
            self.train_model(model, X_train, y_train)
            predictions = self.predict(model, X_test)
            metrics = self.evaluate(y_test, predictions)
            result = ExperimentResult(
                model_name=self.model_name,
                metrics=metrics,
                duration_seconds=self.last_duration_seconds,
                predictions=predictions,
            )
            self.publisher.publish(TrainingEvent(
                "completed", "Experiment completed successfully",
                {"model": self.model_name, "metrics": metrics,
                 "duration_seconds": result.duration_seconds},
            ))
            return result
        except Exception as exc:
            self.publisher.publish(TrainingEvent(
                "failed", f"Experiment failed: {exc}", {"error": str(exc)}
            ))
            raise

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def load_data(self):
        raise NotImplementedError

    def split_data(self, X, y):
        return train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )

    @abstractmethod
    def create_model(self):
        raise NotImplementedError

    @measure_time
    def train_model(self, model, X_train, y_train):
        self.publisher.publish(TrainingEvent("training", "Model training started"))
        model.fit(X_train, y_train)
        self.publisher.publish(TrainingEvent("training", "Model training finished"))

    def predict(self, model, X_test):
        return model.predict(X_test)

    def evaluate(self, y_true, y_pred):
        return calculate_metrics(
            y_true, y_pred, [AccuracyMetric(), F1Metric()]
        )


class IrisExperiment(BaseExperiment):
    """Ready-to-run Iris experiment; model can be selected via constructor."""

    def __init__(self, model_name="logistic_regression", model_params=None,
                 publisher=None):
        super().__init__(publisher=publisher)
        self._model_name = model_name
        self.model_params = model_params or {}

    @property
    def model_name(self):
        return self._model_name

    def load_data(self):
        dataset = load_iris()
        return dataset.data, dataset.target

    def create_model(self):
        return ModelFactory.create(self.model_name, **self.model_params)
