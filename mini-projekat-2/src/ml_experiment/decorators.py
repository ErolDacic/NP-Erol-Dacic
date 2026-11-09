"""Decorator pattern: measure and report the duration of a function."""

from functools import wraps
from time import perf_counter
from .observers import TrainingEvent


def measure_time(function):
    """Measure execution time and attach it to the result/event stream.

    If the decorated instance has a ``publisher`` attribute, a timing event
    is published after successful execution. The original return value stays
    unchanged.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        start = perf_counter()
        result = function(self, *args, **kwargs)
        elapsed = perf_counter() - start
        self.last_duration_seconds = elapsed
        publisher = getattr(self, "publisher", None)
        if publisher is not None:
            publisher.publish(TrainingEvent(
                event_type="timing",
                message=f"{function.__name__} completed in {elapsed:.6f}s",
                details={"function": function.__name__,
                         "duration_seconds": elapsed},
            ))
        return result
    return wrapper
