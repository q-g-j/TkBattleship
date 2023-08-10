from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side
from views.main import Main


class MessageBoxTextSentEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main) -> None:
        self.__main_view = main_view

    def execute(self, side: Side, messages: list[str]) -> None:
        self.__main_view.show_messagebox(side, messages)
