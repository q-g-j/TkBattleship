from models.enums import Event


class EventAggregator:
    def __init__(self) -> None:
        self.__subscribers = {}

    def subscribe(self, event_type: Event, callback) -> None:
        if event_type not in self.__subscribers:
            self.__subscribers[event_type] = []
        self.__subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: Event, callback) -> None:
        if event_type in self.__subscribers:
            self.__subscribers[event_type].remove(callback)

    def publish(self, event_type: Event, *args, **kwargs) -> None:
        if event_type in self.__subscribers:
            for callback in self.__subscribers[event_type]:
                callback(event_type, *args, **kwargs)
