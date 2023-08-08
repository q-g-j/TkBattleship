import tkinter as tk
from tkinter import ttk, Frame
from models.enums import Event
from models.styles import StyleDefinition


class Menu(Frame):
    def __init__(self, field_frame, event_aggregator) -> None:
        self.__event_aggregator = event_aggregator
        super().__init__(field_frame, bg="darkgray", padx=15, pady=15)

    def show(self) -> None:
        label = ttk.Label(self, text="Battle Ship", style=StyleDefinition.MENU_ITEM_HEADER_LABEL)
        label.pack()

        button_singleplayer = ttk.Button(
            self,
            text="Singleplayer",
            style=StyleDefinition.MENU_ITEM_BUTTON,
            command=self.__command_start_singleplayer,
        )

        button_multiplayer = ttk.Button(
            self,
            text="Multiplayer",
            style=StyleDefinition.MENU_ITEM_BUTTON,
            command=self.__command_start_multiplayer,
        )

        button_quit = ttk.Button(
            self,
            text="Quit",
            style=StyleDefinition.MENU_ITEM_BUTTON,
            command=self.__command_quit,
        )
        button_singleplayer.pack(pady=(15, 0))
        # button_multiplayer.pack(pady=(5, 0))
        button_quit.pack(pady=(15, 0))

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def close(self) -> None:
        self.__event_aggregator.publish(Event.MENU_CLOSED)
        self.destroy()

    def __command_start_singleplayer(self) -> None:
        self.__event_aggregator.publish(Event.SINGLEPLAYER_CLICKED)
        self.close()

    def __command_start_multiplayer(self) -> None:
        self.__event_aggregator.publish(Event.MULTIPLAYER_CLICKED)
        self.close()

    def __command_quit(self) -> None:
        self.__event_aggregator.publish(Event.QUIT_BUTTON_CLICKED)


class Lobby(Frame):
    def __init__(self) -> None:
        super().__init__()
