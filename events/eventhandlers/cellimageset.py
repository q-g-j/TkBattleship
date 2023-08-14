from PIL import ImageTk

from models.enums import Side
from models.position import Position
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class CellImageSetEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView) -> None:
        self.__main_view = main_view

    def execute(self, side: Side, pos: Position, image: ImageTk.PhotoImage) -> None:
        self.__main_view.set_cell_image(side, pos, image)
