import tkinter as tk
from tkinter import ttk

from events.eventaggregator import EventAggregator
from factories.commandfactory import CommandFactory
from models.enums import Event, Command
from views.fonts import Fonts
from views.styles import StyleDefinitions
from views.themes import Themes
from views.viewbase import ViewBase


class Menu(ViewBase):
    def __init__(
            self,
            field_frame: ttk.Frame,
            event_aggregator: EventAggregator,
            command_factory: CommandFactory,
            theme: str,
    ) -> None:
        super().__init__(field_frame, command_factory, style=StyleDefinitions.MENU_FRAME, padding=20)
        self.__event_aggregator = event_aggregator
        self.__theme = theme
        self.__theme_var = tk.StringVar()
        self.__theme_var.set("Theme: " + self.__theme)

        # Setup controls:
        label = ttk.Label(
            self,
            text="Battle Ship",
            style=StyleDefinitions.MENU_ITEM_HEADER_LABEL,
            font=(Fonts.TITLE, 20, "bold"),
        )

        button_singleplayer = ttk.Button(
            self,
            text="Singleplayer",
            style=StyleDefinitions.MENU_ITEM_BUTTON,
            takefocus=False,
            command=lambda cmd=Command.START_SINGLE_PLAYER: self._handle_command(cmd),
        )

        # button_multiplayer = ttk.Button(
        #     self,
        #     text="Multiplayer",
        #     style=StyleDefinitions.MENU_ITEM_BUTTON,
        #     takefocus=False,
        #     command=lambda cmd=Command.START_MULTIPLAYER: self._handle_command(cmd)
        # )

        theme_menu = ttk.OptionMenu(
            self,
            self.__theme_var,
            None,
            *Themes.ALL_THEMES,
            direction="right",
            style=StyleDefinitions.MENU_ITEM_THEME_BUTTON,
            command=self.__set_theme
        )

        button_quit = ttk.Button(
            self,
            text="Quit",
            takefocus=False,
            style=StyleDefinitions.MENU_ITEM_QUIT_BUTTON,
            command=lambda cmd=Command.QUIT_GAME: self._handle_command(cmd),
        )

        theme_menu["menu"].configure(font=(Fonts.NORMAL_TEXT, 11))

        label.grid(row=0, column=0, padx=5, pady=5)
        button_singleplayer.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        # button_multiplayer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        theme_menu.grid(row=3, column=0, padx=5, pady=(20, 5), sticky="ew")
        button_quit.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.grid_columnconfigure(0, weight=1)

    def show(self) -> None:
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=250)

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MENU_CLOSED)
        self.destroy()

    def __set_theme(self, _) -> None:
        theme: str = self.__theme_var.get()
        self.__theme_var.set("Theme: {0}".format(theme))
        self._handle_command(Command.CHANGE_THEME, theme)

    def __get_theme_from_var(self) -> str:
        t = self.__theme_var.get().replace("Theme: ", "")
        return t
