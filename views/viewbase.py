from tkinter import Frame

from factories.commandfactory import CommandFactory
from models.enums import Command


class ViewBase(Frame):
    def __init__(self, parent, command_factory: CommandFactory, **kwargs):
        super().__init__(parent, **kwargs)
        self.__command_factory = command_factory

    def handle_command(self, command: Command, *args) -> None:
        command = self.__command_factory.get_command(self.__class__.__name__, command)
        command.execute(*args)
