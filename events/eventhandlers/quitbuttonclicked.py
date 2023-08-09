from tkinter import Tk

from events.eventhandlers.eventhandlerbase import EventHandlerBase


class QuitButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, root: Tk) -> None:
        self.__root = root

    def execute(self):
        self.__root.destroy()
