from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class MessageBoxCloseRequestedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView) -> None:
        self.__main_view = main_view

    def execute(self) -> None:
        self.__main_view.close_messagebox()
