from ttkthemes import ThemedTk
from events.eventhandlers.eventhandlerbase import EventHandlerBase


class QuitButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, root: ThemedTk) -> None:
        self.__root = root

    def execute(self):
        self.__root.destroy()
