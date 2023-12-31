from tkinter import ttk

from factories.commandfactory import CommandFactory
from models.enums import Command, Side
from models.position import Position
from views.styles import StyleDefinitions
from views.viewbase import ViewBase


class Cell(ViewBase):
    def __init__(
        self, parent: ttk.Frame, command_factory: CommandFactory, side: Side, pos: Position, cell_size: int, **kwargs
    ) -> None:
        super().__init__(parent, command_factory, width=cell_size, height=cell_size, padding=(0, 0, 0, 0), **kwargs)
        self.grid(row=pos.row, column=pos.col, padx=0, pady=0)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.button = ttk.Button(self, takefocus=False, style=StyleDefinitions.CELL_BUTTON)
        self.button.grid(sticky="wens")
        self.button.config(
            command=lambda cmd=Command.CELL_CLICK, s=side, p=pos: self._handle_command(cmd, s, p),
        )
