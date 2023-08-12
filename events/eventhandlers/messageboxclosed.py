from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class MessageBoxCloseRequestedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, event_aggregator: EventAggregator) -> None:
        self.__main_view = main_view
        self.__event_aggregator = event_aggregator

    def execute(self):
        self.__main_view.close_messagebox()
