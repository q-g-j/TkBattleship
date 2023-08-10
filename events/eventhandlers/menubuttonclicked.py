from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import GameState
from models.game import Game
from views.main import Main


class MenuButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main, game: Game) -> None:
        self.__main_view = main_view
        self.__game = game

    def execute(self):
        if self.__main_view.is_messagebox_open:
            self.__main_view.close_messagebox()
        if not self.__main_view.is_menu_open:
            self.__main_view.show_menu()
            self.__main_view.is_menu_open = True
        else:
            if self.__game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()
