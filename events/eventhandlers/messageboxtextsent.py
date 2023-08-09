from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side
from views.mainview import MainView


class MessageBoxTextSentEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView) -> None:
        self.__main_view = main_view

    def execute(self, side: Side, messages: list) -> None:
        self.__main_view.show_messagebox(side, messages)
