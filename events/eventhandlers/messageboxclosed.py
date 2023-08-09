from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class MessageBoxClosedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView) -> None:
        self.__main_view = main_view

    def execute(self):
        self.__main_view.is_messagebox_open = False
