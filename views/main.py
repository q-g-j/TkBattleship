import tkinter as tk
from tkinter import Tk, ttk
from PIL import ImageTk

from factories.commandfactory import CommandFactory
from models.images import Images
from events.eventaggregator import EventAggregator
from models.enums import Command, Orientation, NotationColumns, Side
from models.position import Position
from models.ship import Ship
from models.settings import Settings
from views.cell import Cell
from views.menu import Menu
from views.messagebox import Messagebox
from models.styles import StyleDefinition
from views.viewbase import ViewBase
from utils.sleep import threaded_sleep


class Main(ViewBase):
    def __init__(
        self,
        root: Tk,
        event_aggregator: EventAggregator,
        command_factory: CommandFactory,
        settings: Settings,
    ) -> None:
        super().__init__(root, command_factory)
        self.__event_aggregator = event_aggregator
        self.__command_factory = command_factory
        self.__settings = settings
        self.__game_frame = ttk.Frame(self)
        self.__toolbar_frame = ttk.Frame(self)
        self.__menu_button = ttk.Button(
            self.__toolbar_frame,
            text="Menu",
            command=lambda cmd=Command.MENU_BUTTON_CLICKED: self._handle_command(cmd),
            style=StyleDefinition.MENU_BUTTON,
        )
        self.__random_ships_button = ttk.Button(
            self.__toolbar_frame,
            text="Random ships",
            command=lambda cmd=Command.RANDOM_SHIPS_BUTTON_CLICKED: self._handle_command(
                cmd
            ),
            style=StyleDefinition.RANDOM_SHIPS_BUTTON,
        )
        self.__status_label = ttk.Label(
            self.__toolbar_frame,
            style=StyleDefinition.STATUS_LABEL
        )
        self.__menu_button.grid(row=0, column=0)
        self.__status_label.grid(row=0, column=2)
        self.__toolbar_frame.pack(anchor=tk.W)
        self.__game_frame.pack(pady=(10, 0))
        self.__menu: Menu | None = None
        self.__messagebox: Messagebox | None = None
        self.__field_frame_left: ttk.Frame | None = None
        self.__field_frame_right: ttk.Frame | None = None
        self.__cells_opponent: list[list[Cell]] = []
        self.__cells_player: list[list[Cell]] = []
        self.__create_playing_fields()
        self.__create_notation()
        self.__create_cells()
        self.pack(padx=20, pady=20)

        self.is_menu_open = False
        self.is_messagebox_open = False

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
            label = ttk.Label(frame, text=text, anchor=tk.CENTER)
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

    def change_random_ships_button_visibility(self, toggle: bool):
        if toggle:
            self.__random_ships_button.grid(row=0, column=1, padx=(10, 0))
        else:
            self.__random_ships_button.grid_forget()

    def show_menu(self, delay: float = 0) -> None:
        self.__menu = Menu(
            self.__game_frame, self.__event_aggregator, self.__command_factory
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

    def set_cell_image(
        self, side: Side, pos: Position, image: ImageTk.PhotoImage
    ) -> None:
        if side == Side.LEFT:
            cells = self.__cells_player
        elif side == Side.RIGHT:
            cells = self.__cells_opponent
        else:
            raise Exception(
                'Invalid value for param "side". Must be Side.LEFT or Side.RIGHT.'
            )
        cells[pos.row][pos.col].button.config(image=image)

    def mark_ship_destroyed(self, side: Side, ship: Ship) -> None:
        if side == Side.LEFT:
            cells = self.__cells_player
        elif side == Side.RIGHT:
            cells = self.__cells_opponent
        else:
            raise Exception(
                'Invalid value for param "side". Must be Side.LEFT or Side.RIGHT.'
            )
        for hit_pos in ship.hit_positions:
            cells[hit_pos.row][hit_pos.col].button.config(image=Images.DESTROYED)

    def set_status_label_text(self, text: str):
        self.__status_label.config(text=text)

    def show_messagebox(self, side: Side, messages: list) -> None:
        frame: ttk.Frame | None = None
        if side == Side.LEFT:
            frame = self.__field_frame_left
        elif side == Side.RIGHT:
            frame = self.__field_frame_right
        elif side == Side.BOTH:
            frame = self.__game_frame

        if self.__messagebox is not None:
            self.is_messagebox_open = False
            self.__messagebox.close()
        self.__messagebox = Messagebox(
            frame, self.__event_aggregator, self.__command_factory
        )
        self.__messagebox.show(messages)
        self.is_messagebox_open = True

    def close_messagebox(self) -> None:
        self.__messagebox.close()
