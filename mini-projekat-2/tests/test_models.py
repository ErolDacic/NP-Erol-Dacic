import pytest
from ml_experiment.models import ModelFactory
from sklearn.base import ClassifierMixin


@pytest.mark.parametrize("name", ["logistic_regression", "decision_tree", "knn"])
def test_factory_creates_classifier(name):
    assert isinstance(ModelFactory.create(name), ClassifierMixin)


def test_factory_rejects_unknown_model():
    with pytest.raises(ValueError, match="Unsupported model"):
        ModelFactory.create("random_forest_that_does_not_exist")


def test_factory_returns_fresh_instances():
    assert ModelFactory.create("knn") is not ModelFactory.create("knn")
