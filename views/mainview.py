import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from ttkthemes import ThemedTk

from events.eventaggregator import EventAggregator
from factories.commandfactory import CommandFactory
from models.enums import Command, Orientation, NotationColumns, Side, Event
from models.position import Position
from models.ship import Ship
from services.injector import inject
from settings.settingsreader import SettingsReader
from utils.sleep import threaded_sleep
from views.cell import Cell
from views.fonts import Fonts
from views.images import Images
from views.menu import Menu
from views.messagebox import MessageBox
from views.styles import StyleDefinitions
from views.viewbase import ViewBase


@inject(ThemedTk, EventAggregator, CommandFactory, SettingsReader)
class MainView(ViewBase):
    def __init__(
            self,
            root: ThemedTk,
            event_aggregator: EventAggregator,
            command_factory: CommandFactory,
            settings_reader: SettingsReader,
    ) -> None:
        super().__init__(root, command_factory, style=StyleDefinitions.MAIN_VIEW_FRAME, padding=20)
        self.__event_aggregator = event_aggregator
        self.__command_factory = command_factory
        self.__settings_reader = settings_reader
        self.__settings = settings_reader.read()
        self.__game_frame = ttk.Frame(self)
        self.__toolbar_frame = ttk.Frame(self)
        self.__menu_button = ttk.Button(
            self.__toolbar_frame,
            text="MENU",
            takefocus=False,
            command=lambda cmd=Command.OPEN_MENU: self._handle_command(cmd),
            style=StyleDefinitions.MENU_BUTTON,
        )
        self.__random_ships_button = ttk.Button(
            self.__toolbar_frame,
            text="Random ships",
            takefocus=False,
            command=lambda cmd=Command.PLACE_RANDOM_SHIPS: self._handle_command(cmd),
            style=StyleDefinitions.RANDOM_SHIPS_BUTTON,
        )
        self.__status_label = ttk.Label(
            self.__toolbar_frame,
            style=StyleDefinitions.STATUS_LABEL,
            font=(Fonts.NORMAL_TEXT, 12),
            foreground="blue",
        )

        self.__toolbar_frame.pack(anchor=tk.W, padx=(40, 0), ipadx=10)

        self.__menu_button.grid(row=0, column=0)
        self.__status_label.grid(row=0, column=2, padx=(15, 0))

        self.__game_frame.pack(pady=(10, 0))
        self.__menu: Menu | None = None
        self.__messagebox: MessageBox | None = None
        self.__field_frame_left: ttk.Frame | None = None
        self.__field_frame_right: ttk.Frame | None = None
        self.__cells_opponent: list[list[Cell]] = []
        self.__cells_player: list[list[Cell]] = []
        self.__create_playing_fields()
        self.__create_notation()
        self.__create_cells()
        self.pack()

        self.is_menu_open = False
        self.is_messagebox_open = False
        self.__is_ai_next = False

    def __create_playing_fields(self) -> None:
        self.__field_frame_left = ttk.Frame(self.__game_frame)
        self.__field_frame_left.grid(row=1, column=1, rowspan=10, columnspan=10)

        self.__field_frame_right = ttk.Frame(self.__game_frame)
        self.__field_frame_right.grid(row=1, column=12, rowspan=10, columnspan=10)

    def __create_notation(self) -> None:
        def create_notation_cell(direction, row, column):
            frame = ttk.Frame(
                self.__game_frame,
                width=self.__settings.cell_size,
                height=self.__settings.cell_size,
                style=StyleDefinitions.NOTATION_FRAME
            )
            frame.grid(row=row, column=column)
            frame.grid_propagate(False)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            text = (
                str(row)
                if direction == Orientation.VERTICAL
                else NotationColumns[column if column < 11 else column - 11]
            )
            label = ttk.Label(frame, text=text, anchor=tk.CENTER, font=(Fonts.NORMAL_TEXT, 10))
            label.grid(sticky="wens")

        for i in range(1, 11):
            create_notation_cell(Orientation.HORIZONTAL, 0, i)
            create_notation_cell(Orientation.HORIZONTAL, 11, i)
            create_notation_cell(Orientation.VERTICAL, i, 0)
            create_notation_cell(Orientation.VERTICAL, i, 11)
            create_notation_cell(Orientation.HORIZONTAL, 0, i + 11)
            create_notation_cell(Orientation.HORIZONTAL, 11, i + 11)
            create_notation_cell(Orientation.VERTICAL, i, 22)

    def __create_cells(self) -> None:
        sides = [
            (Side.LEFT, self.__field_frame_left, self.__cells_player),
            (Side.RIGHT, self.__field_frame_right, self.__cells_opponent),
        ]

        for item in sides:
            side: Side = item[0]
            field_frame: ttk.Frame = item[1]
            cells: list[list[Cell]] = item[2]

            for row in range(0, 10):
                inner_list: list[Cell] = []
                for column in range(0, 10):
                    pos = Position(row, column)
                    cell = Cell(
                        field_frame,
                        self.__command_factory,
                        side,
                        pos,
                        self.__settings.cell_size,
                    )
                    inner_list.append(cell)
                cells.append(inner_list)

    def change_random_ships_button_visibility(self, toggle: bool) -> None:
        if toggle:
            self.__random_ships_button.grid(row=0, column=1, padx=(10, 0), ipadx=10)
        else:
            self.__random_ships_button.grid_forget()

    def show_menu(self, delay: float = 0) -> None:
        self.__settings = self.__settings_reader.read()
        self.__menu = Menu(
            self.__game_frame,
            self.__event_aggregator,
            self.__command_factory,
            self.__settings.theme,
        )
        if delay > 0:
            threaded_sleep(lambda: self.__menu.show(), delay)
        else:
            self.__menu.show()
        self.is_menu_open = True

    def close_menu(self) -> None:
        self.__menu.close()

    def clear_cells(self, side: Side) -> None:
        for row in range(10):
            for column in range(10):
                if side & Side.LEFT == Side.LEFT:
                    self.__cells_player[row][column].button.config(image=Images.EMPTY)
                if side & Side.RIGHT == Side.RIGHT:
                    self.__cells_opponent[row][column].button.config(image=Images.EMPTY)

    def set_cell_image(self, side: Side, pos: Position, image: ImageTk.PhotoImage) -> None:
        if side == Side.LEFT:
            cells = self.__cells_player
        elif side == Side.RIGHT:
            cells = self.__cells_opponent
        else:
            raise Exception('Invalid value for param "side". Must be Side.LEFT or Side.RIGHT.')
        cells[pos.row][pos.col].button.config(image=image)

    def mark_ship_destroyed(self, side: Side, ship: Ship) -> None:
        if side == Side.LEFT:
            cells = self.__cells_player
        elif side == Side.RIGHT:
            cells = self.__cells_opponent
        else:
            raise Exception('Invalid value for param "side". Must be Side.LEFT or Side.RIGHT.')
        for hit_pos in ship.hit_positions:
            cells[hit_pos.row][hit_pos.col].button.config(image=Images.DESTROYED)

    def set_status_label_text(self, text: str) -> None:
        self.__status_label.configure(text=text)

    def show_messagebox(self, side: Side, messages: list, ai_next=False) -> None:
        self.__is_ai_next = ai_next
        frame: ttk.Frame | None = None
        if side == Side.LEFT:
            frame = self.__field_frame_left
        elif side == Side.RIGHT:
            frame = self.__field_frame_right
        elif side == Side.BOTH:
            frame = self.__game_frame

        self.close_messagebox()
        self.is_messagebox_open = True
        self.__messagebox = MessageBox(frame, self.__event_aggregator, self.__command_factory)
        self.__messagebox.show(messages)

    def close_messagebox(self) -> None:
        if self.__messagebox is not None:
            self.is_messagebox_open = False
            self.__messagebox.destroy()
            self.__messagebox = None
            if self.__is_ai_next:
                self.__event_aggregator.publish(Event.AI_NEXT_MOVE_REQUESTED)
                self.__is_ai_next = False
