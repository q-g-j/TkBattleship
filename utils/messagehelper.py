from models.enums import Event, Side
from events.eventaggregator import EventAggregator
from utils.sleep import threaded_sleep
from services.injector import inject


@inject(EventAggregator)
class MessageHelper:
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def show(self, side: Side, messages: list, delay: float = 0, ai_next=False) -> None:
        if delay > 0:
            threaded_sleep(
                lambda: self.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages, ai_next),
                delay,
            )
        else:
            self.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages, ai_next)
