import pytest
from ml_experiment.metrics import (
    AccuracyMetric, F1Metric, PrecisionMetric, RecallMetric, calculate_metrics
)


def test_metrics_return_expected_perfect_scores():
    y = [0, 1, 2, 0, 1, 2]
    strategies = [AccuracyMetric(), F1Metric(), PrecisionMetric(), RecallMetric()]
    scores = calculate_metrics(y, y, strategies)
    assert set(scores) == {"accuracy", "f1", "precision", "recall"}
    assert all(score == pytest.approx(1.0) for score in scores.values())


def test_metrics_require_at_least_one_strategy():
    with pytest.raises(ValueError):
        calculate_metrics([0, 1], [0, 1], [])
