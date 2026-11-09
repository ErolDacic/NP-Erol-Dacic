"""Command-line demonstration of the framework on the Iris dataset."""

import argparse
from .experiment import IrisExperiment
from .observers import ConsoleObserver, EventPublisher


def main():
    parser = argparse.ArgumentParser(description="Run an Iris ML experiment.")
    parser.add_argument(
        "--model", default="logistic_regression",
        choices=ModelFactoryChoices,
        help="Classifier to train."
    )
    args = parser.parse_args()

    publisher = EventPublisher()
    publisher.attach(ConsoleObserver())
    result = IrisExperiment(model_name=args.model, publisher=publisher).run()

    print("\nResults")
    print(f"Model: {result.model_name}")
    for metric, value in result.metrics.items():
        print(f"{metric}: {value:.4f}")
    print(f"Training time: {result.duration_seconds:.6f} seconds")


# Kept explicit so argparse displays valid choices without creating a model.
ModelFactoryChoices = ("logistic_regression", "decision_tree", "knn")

if __name__ == "__main__":
    main()
