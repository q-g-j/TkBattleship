from tkinter import ttk

from factories.commandfactory import CommandFactory
from models.enums import Command


class ViewBase(ttk.Frame):
    def __init__(self, parent, command_factory: CommandFactory, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.__command_factory = command_factory

    def _handle_command(self, command: Command, *args) -> None:
        command = self.__command_factory.get_command(self.__class__.__name__, command)
        command.execute(*args)
