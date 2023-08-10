from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.main import Main


class RandomShipsButtonVisiblityChangedEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main) -> None:
        self.__main_view = main_view

    def execute(self, toggle: bool) -> None:
        self.__main_view.change_random_ships_button_visibility(toggle)
