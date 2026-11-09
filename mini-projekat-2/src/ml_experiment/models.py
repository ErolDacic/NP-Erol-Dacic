"""Factory pattern: centralised creation of scikit-learn estimators."""

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


class ModelFactory:
    """Creates supported classifiers by a short, stable model name."""

    _SUPPORTED = ("logistic_regression", "decision_tree", "knn")

    @classmethod
    def create(cls, model_name: str, **params):
        """Return a fresh estimator. Raises ValueError for unknown names."""
        name = model_name.strip().lower()
        if name == "logistic_regression":
            defaults = {"max_iter": 1000, "random_state": 42}
            defaults.update(params)
            return LogisticRegression(**defaults)
        if name == "decision_tree":
            defaults = {"random_state": 42}
            defaults.update(params)
            return DecisionTreeClassifier(**defaults)
        if name == "knn":
            defaults = {"n_neighbors": 5}
            defaults.update(params)
            return KNeighborsClassifier(**defaults)
        raise ValueError(
            f"Unsupported model '{model_name}'. Choose one of: "
            + ", ".join(cls._SUPPORTED)
        )

    @classmethod
    def supported_models(cls):
        return cls._SUPPORTED
