"""Observer pattern: publish training lifecycle events to subscribers."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class TrainingEvent:
    event_type: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


class Observer:
    """Observer interface."""

    def update(self, event: TrainingEvent) -> None:
        raise NotImplementedError


class EventPublisher:
    """Subject that manages observers and broadcasts events."""

    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, event: TrainingEvent) -> None:
        for observer in tuple(self._observers):
            observer.update(event)


class ConsoleObserver(Observer):
    def update(self, event: TrainingEvent) -> None:
        print(f"[{event.event_type}] {event.message}")


class HistoryObserver(Observer):
    """Stores events in memory; useful for tests and later reporting."""

    def __init__(self):
        self.events = []

    def update(self, event: TrainingEvent) -> None:
        self.events.append(event)
