from PIL import ImageTk

from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side
from views.mainview import MainView


class CellImageSetEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView) -> None:
        self.__main_view = main_view

    def execute(self, side: Side, row: int, column: int, image: ImageTk.PhotoImage
    ) -> None:
        self.__main_view.set_cell_image(side, row, column, image)
