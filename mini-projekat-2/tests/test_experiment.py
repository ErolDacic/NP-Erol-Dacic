from ml_experiment.experiment import IrisExperiment
from ml_experiment.observers import EventPublisher, HistoryObserver


def test_iris_experiment_returns_metrics_and_predictions():
    result = IrisExperiment().run()
    assert result.model_name == "logistic_regression"
    assert 0.0 <= result.metrics["accuracy"] <= 1.0
    assert 0.0 <= result.metrics["f1"] <= 1.0
    assert len(result.predictions) == 38


def test_experiment_publishes_lifecycle_and_timing_events():
    publisher = EventPublisher()
    history = HistoryObserver()
    publisher.attach(history)
    result = IrisExperiment("knn", publisher=publisher).run()
    event_types = [event.event_type for event in history.events]
    assert "started" in event_types
    assert "training" in event_types
    assert "timing" in event_types
    assert "completed" in event_types
    assert result.duration_seconds >= 0
