from PIL import ImageTk

from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side
from models.position import Position
from views.main import Main


class CellImageSetEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main) -> None:
        self.__main_view = main_view

    def execute(self, side: Side, pos: Position, image: ImageTk.PhotoImage
    ) -> None:
        self.__main_view.set_cell_image(side, pos, image)
