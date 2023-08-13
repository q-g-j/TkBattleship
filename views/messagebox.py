import tkinter as tk
from tkinter import ttk

from factories.commandfactory import CommandFactory
from models.enums import Event
from events.eventaggregator import EventAggregator
from views.fonts import Fonts
from views.styles import StyleDefinitions
from views.viewbase import ViewBase


class MessageBox(ViewBase):
    def __init__(self, parent: ttk.Frame, event_aggregator: EventAggregator, command_factory: CommandFactory) -> None:
        self.__event_aggregator = event_aggregator
        super().__init__(parent, command_factory, style=StyleDefinitions.MESSAGEBOX_FRAME, padding=20)

    def show(self, messages: list) -> None:
        for message in messages:
            label = ttk.Label(self, text=message, style=StyleDefinitions.MESSAGEBOX_LABEL, font=(Fonts.SELAWIK, 13),
                              foreground="black", )
            label.pack(expand=True, anchor=tk.CENTER)
        close = ttk.Button(
            self, text="Close", command=self.close, style=StyleDefinitions.MESSAGEBOX_BUTTON
        )
        close.pack(pady=(10, 0))
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MESSAGEBOX_CLOSE_REQUESTED)
