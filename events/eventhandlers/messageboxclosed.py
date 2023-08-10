from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.main import Main


class MessageBoxClosedEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main) -> None:
        self.__main_view = main_view

    def execute(self):
        self.__main_view.is_messagebox_open = False
