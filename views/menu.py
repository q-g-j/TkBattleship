import tkinter as tk
from tkinter import ttk

from events.eventaggregator import EventAggregator
from factories.commandfactory import CommandFactory
from models.enums import Event, Command
from models.styles import StyleDefinition
from views.viewbase import ViewBase


class Menu(ViewBase):
    def __init__(self, field_frame: ttk.Frame, event_aggregator: EventAggregator,
                 command_factory: CommandFactory) -> None:
        self.__event_aggregator = event_aggregator
        super().__init__(field_frame, command_factory, bg="darkgray", padx=15, pady=15)

    def show(self) -> None:
        label = ttk.Label(self, text="Battle Ship", style=StyleDefinition.MENU_ITEM_HEADER_LABEL)
        label.pack()

        button_singleplayer = ttk.Button(
            self,
            text="Singleplayer",
            style=StyleDefinition.MENU_ITEM_BUTTON,
            command=lambda cmd=Command.START_SINGLEPLAYER: self._handle_command(cmd)
        )

        # button_multiplayer = ttk.Button(
        #     self,
        #     text="Multiplayer",
        #     style=StyleDefinition.MENU_ITEM_BUTTON,
        #     command=lambda cmd=Command.START_MULTIPLAYER: self.handle_command(cmd)
        # )

        button_quit = ttk.Button(
            self,
            text="Quit",
            style=StyleDefinition.MENU_ITEM_BUTTON,
            command=lambda cmd=Command.QUIT_GAME: self._handle_command(cmd),
        )
        button_singleplayer.pack(pady=(15, 0))
        # button_multiplayer.pack(pady=(5, 0))
        button_quit.pack(pady=(15, 0))

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MENU_CLOSED)
        self.destroy()


class Lobby(ttk.Frame):
    def __init__(self) -> None:
        super().__init__()
