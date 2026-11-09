from ml_experiment.observers import EventPublisher, HistoryObserver, TrainingEvent


def test_publisher_notifies_attached_observer():
    publisher = EventPublisher()
    observer = HistoryObserver()
    publisher.attach(observer)
    publisher.publish(TrainingEvent("test", "hello"))
    assert len(observer.events) == 1
    assert observer.events[0].message == "hello"


def test_detached_observer_receives_no_events():
    publisher = EventPublisher()
    observer = HistoryObserver()
    publisher.attach(observer)
    publisher.detach(observer)
    publisher.publish(TrainingEvent("test", "hello"))
    assert observer.events == []
