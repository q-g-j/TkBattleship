from models.enums import Side
from events.eventaggregator import EventAggregator
from utils.sleep import threaded_sleep
from services.injector import inject


@inject(EventAggregator)
class MessageHelper:
    def __init__(self, event_aggregator: EventAggregator):
        self.__event_aggregator = event_aggregator

    def show(self, side: Side, messages: list, delay: float = 0) -> None:
        from models.enums import Event
        if delay > 0:
            threaded_sleep(lambda: self.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages),
                           delay)
        else:
            self.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages)
