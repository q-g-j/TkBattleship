from events.eventhandlers.eventhandlerbase import EventHandlerBase
from ttkthemes import ThemedTk


class QuitButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, root: ThemedTk) -> None:
        self.__root = root

    def execute(self) -> None:
        self.__root.destroy()
