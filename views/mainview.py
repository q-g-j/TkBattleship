import tkinter as tk
from tkinter import Tk, ttk, Frame
from PIL import ImageTk

from factories.commandfactory import CommandFactory
from models.images import Images
from events.eventaggregator import EventAggregator
from models.enums import *
from models.position import Position
from models.ship import Ship
from utils.sleep import threaded_sleep
from views.menuview import Menu
from views.messageboxview import Messagebox
from models.styles import StyleDefinition
from views.viewbase import ViewBase


class MainView(ViewBase):
    def __init__(self, root: Tk, event_aggregator: EventAggregator, command_factory: CommandFactory) -> None:
        super().__init__(root, command_factory)
        self.__event_aggregator = event_aggregator
        self.__command_factory = command_factory
        self.__game_frame = Frame(self)
        self.__toolbar_frame = Frame(self)
        self.__menu_button = ttk.Button(
            self.__toolbar_frame,
            text="Menu",
            command=lambda cmd=Command.MENU_BUTTON_CLICKED: self._handle_command(cmd),
            style=StyleDefinition.MENU_BUTTON,
        )
        self.__random_ships_button = ttk.Button(
            self.__toolbar_frame,
            text="Random ships",
            command=lambda cmd=Command.RANDOM_SHIPS_BUTTON_CLICKED: self._handle_command(cmd),
            style=StyleDefinition.MENU_BUTTON,
        )
        self.__menu_button.grid(row=0, column=0)
        self.__toolbar_frame.pack(anchor=tk.W)
        self.__game_frame.pack(pady=(10, 0))
        self.__menu = None
        self.__messagebox = None
        self.__field_frame_left = None
        self.__field_frame_right = None
        self.__cells_opponent = []
        self.__cells_player = []
        self.__create_playing_fields()
        self.__create_notation()
        self.__create_cells(Side.LEFT)
        self.__create_cells(Side.RIGHT)
        self.pack(padx=20, pady=20)

        self.is_menu_open = False
        self.is_messagebox_open = False

    def __create_playing_fields(self) -> None:
        self.__field_frame_left = Frame(self.__game_frame)
        self.__field_frame_left.grid(row=1, column=1, rowspan=10, columnspan=10)

        self.__field_frame_right = Frame(self.__game_frame)
        self.__field_frame_right.grid(row=1, column=12, rowspan=10, columnspan=10)

    def __create_notation(self) -> None:
        def create_notation(direction, row, column):
            frame = Frame(self.__game_frame, width=40, height=40)
            frame.grid(row=row, column=column)
            frame.grid_propagate(False)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            text = (
                str(row)
                if direction == tk.VERTICAL
                else NotationColumns[column if column < 11 else column - 11]
            )
            label = ttk.Label(frame, text=text, anchor=tk.CENTER)
            label.grid(sticky="wens")

        for i in range(1, 11):
            create_notation(tk.HORIZONTAL, 0, i)
            create_notation(tk.HORIZONTAL, 11, i)
            create_notation(tk.VERTICAL, i, 0)
            create_notation(tk.VERTICAL, i, 11)
            create_notation(tk.HORIZONTAL, 0, i + 11)
            create_notation(tk.HORIZONTAL, 11, i + 11)
            create_notation(tk.VERTICAL, i, 22)

    def __create_cells(self, side: Side) -> None:
        if side == Side.LEFT:
            field_frame = self.__field_frame_left
            cells = self.__cells_player
        else:
            field_frame = self.__field_frame_right
            cells = self.__cells_opponent

        for row in range(0, 10):
            inner_list = []
            for column in range(0, 10):
                frame = Frame(field_frame, width=40, height=40)
                frame.grid(column=column, row=row, padx=0, pady=0)
                frame.grid_propagate(False)
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)
                cell = ttk.Button(frame)
                cell.grid(sticky="wens")
                pos = Position(row, column)
                cell.config(
                    command=lambda cmd=Command.CELL_CLICKED, s=side, p=pos:
                    self._handle_command(cmd, s, p),
                )
                inner_list.append(cell)
            cells.append(inner_list)

    def change_random_ships_button_visibility(self, toggle: bool):
        if toggle:
            self.__random_ships_button.grid(row=0, column=1, padx=(10, 0))
        else:
            self.__random_ships_button.grid_forget()

    def show_menu(self, delay: float = 0) -> None:
        self.__menu = Menu(self.__game_frame, self.__event_aggregator, self.__command_factory)
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
                    self.__cells_player[row][column].config(image=Images.EMPTY)
                if side & Side.RIGHT == Side.RIGHT:
                    self.__cells_opponent[row][column].config(image=Images.EMPTY)

    def set_cell_image(self, player_type: Side, pos: Position, image: ImageTk.PhotoImage) -> None:
        if player_type == Side.LEFT:
            cells = self.__cells_player
        else:
            cells = self.__cells_opponent
        cells[pos.row][pos.col].config(image=image)

    def mark_ship_destroyed(
            self, side: Side, ship: Ship) -> None:
        if side == Side.LEFT:
            cells = self.__cells_player
        else:
            cells = self.__cells_opponent
        for hit_pos in ship.hit_positions:
            cells[hit_pos.row][hit_pos.col].config(image=Images.DESTROYED)

    def show_messagebox(self, side: Side, messages: list) -> None:
        if side == Side.LEFT:
            frame = self.__field_frame_left
        elif side == Side.RIGHT:
            frame = self.__field_frame_right
        else:
            frame = self.__game_frame
        if self.__messagebox is not None:
            self.is_messagebox_open = False
            self.__messagebox.close()
        self.__messagebox = Messagebox(frame, self.__event_aggregator, self.__command_factory)
        self.__messagebox.show(messages)
        self.is_messagebox_open = True

    def close_messagebox(self) -> None:
        self.__messagebox.close()
