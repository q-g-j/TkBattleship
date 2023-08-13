import re
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from events.eventaggregator import EventAggregator
from factories.commandfactory import CommandFactory
from models.enums import Event, Command
from settings.settingswriter import SettingsWriter
from views.fonts import Fonts
from views.styles import StyleDefinitions
from views.viewbase import ViewBase


class Menu(ViewBase):
    def __init__(
        self,
        root: ThemedTk,
        field_frame: ttk.Frame,
        event_aggregator: EventAggregator,
        command_factory: CommandFactory,
        theme: str
    ) -> None:
        super().__init__(field_frame, command_factory, style=StyleDefinitions.MENU_FRAME, padding=20)
        self.__root = root
        self.__event_aggregator = event_aggregator
        self.__theme_var = tk.StringVar()
        self.__theme_var.set(theme)

    def show(self) -> None:
        label = ttk.Label(
            self, text="Battle Ship", style=StyleDefinitions.MENU_ITEM_HEADER_LABEL, font=(Fonts.SELAWIK, 18, "bold")
        )
        label.pack()

        button_singleplayer = ttk.Button(
            self,
            text="Singleplayer",
            style=StyleDefinitions.MENU_ITEM_BUTTON,
            command=lambda cmd=Command.START_SINGLEPLAYER: self._handle_command(cmd),
        )

        # button_multiplayer = ttk.Button(
        #     self,
        #     text="Multiplayer",
        #     style=StyleDefinition.MENU_ITEM_BUTTON,
        #     command=lambda cmd=Command.START_MULTIPLAYER: self.handle_command(cmd)
        # )

        # I picked some from ThemedTk that actually work with this app:
        possible_themes = [
            "alt",
            "default",
            "keramik",
            "plastik",
            "scidblue",
            "scidgreen",
            "scidgrey",
            "scidmint",
            "scidpink",
            "scidpurple",
            "scidsand",
            "vista",
            "winnative",
            "winxpblue",
            "xpnative",
        ]
        available_themes = sorted(self.__root.get_themes())

        themes = ["Theme: " + theme for theme in available_themes if theme in possible_themes]

        self.__theme_menu = ttk.OptionMenu(
            self,
            self.__theme_var,
            None,
            *themes,
            direction="right",
            style=StyleDefinitions.MENU_ITEM_BUTTON,
            command=self.__set_theme
        )

        button_quit = ttk.Button(
            self,
            text="Quit",
            style=StyleDefinitions.MENU_ITEM_BUTTON,
            command=lambda cmd=Command.QUIT_GAME: self._handle_command(cmd),
        )
        button_singleplayer.pack(pady=(15, 0))
        # button_multiplayer.pack(pady=(5, 0))
        self.__theme_menu.pack(pady=(5, 0))
        button_quit.pack(pady=(15, 0))

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def __set_theme(self, *args):
        self.__event_aggregator.publish(Event.THEME_CHANGE_REQUESTED, self.__theme_var.get().replace("Theme: ", ""))

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MENU_CLOSED)
        self.destroy()


class Lobby(ttk.Frame):
    def __init__(self) -> None:
        super().__init__()
