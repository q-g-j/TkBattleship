from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import GameState
from store.gamestore import GameStore
from views.mainview import MainView


class MenuButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game_store: GameStore) -> None:
        self.__main_view = main_view
        self.__game_store = game_store

    def execute(self):
        if self.__main_view.is_messagebox_open:
            self.__main_view.close_messagebox()
        if not self.__main_view.is_menu_open:
            self.__main_view.show_menu()
            self.__main_view.is_menu_open = True
        else:
            if self.__game_store.game is not None:
                if self.__game_store.game.game_state != GameState.FIRST_RUN:
                    self.__main_view.close_menu()
