from models.enums import Side
from events.eventaggregator import EventAggregator
from utils.sleep import threaded_sleep
from services.injector import inject


@inject("event_aggregator")
class MessageHelper:
    __event_aggregator = None

    @staticmethod
    def init(event_aggregator: EventAggregator) -> None:
        MessageHelper.__event_aggregator = event_aggregator

    @staticmethod
    def show(side: Side, messages: list, delay: float = 0) -> None:
        from models.enums import Event
        if delay > 0:
            threaded_sleep(lambda: MessageHelper.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages),
                           delay)
        else:
            MessageHelper.__event_aggregator.publish(Event.MESSAGEBOX_TEXT_SENT, side, messages)
