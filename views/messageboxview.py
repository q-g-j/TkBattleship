import tkinter as tk
from tkinter import ttk, Frame

from factories.commandfactory import CommandFactory
from models.enums import Event
from events.eventaggregator import EventAggregator
from models.styles import StyleDefinition
from views.viewbase import ViewBase


class Messagebox(ViewBase):
    def __init__(self, parent: Frame, event_aggregator: EventAggregator, command_factory: CommandFactory) -> None:
        self.__event_aggregator = event_aggregator
        self.__command_factory = command_factory
        super().__init__(parent, command_factory, bg="darkgray", padx=15, pady=15)

    def show(self, messages: list) -> None:
        for message in messages:
            label = ttk.Label(self, text=message, style=StyleDefinition.MESSAGEBOX_LABEL)
            label.pack(expand=True, anchor=tk.CENTER)
        close = ttk.Button(
            self, text="Close", command=self.close, style=StyleDefinition.MESSAGEBOX_BUTTON
        )
        close.pack(pady=(10, 0))
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MESSAGEBOX_CLOSED)
        self.destroy()
