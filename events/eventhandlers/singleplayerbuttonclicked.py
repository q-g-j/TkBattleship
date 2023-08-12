from events.eventhandlers.eventhandlerbase import EventHandlerBase
from factories.gamefactory import GameFactory
from models.debug import Debug
from models.enums import Side
from models.validator import Validator
from store.gamestore import GameStore
from views.mainview import MainView


class SinglePlayerButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game_factory: GameFactory, game_store: GameStore, validator: Validator):
        self.__main_view = main_view
        self.__game_factory = game_factory
        self.__game_store = game_store
        self.__validator = validator

    def execute(self):
        self.__main_view.close_menu()
        self.__main_view.clear_cells(Side.BOTH)
        self.__game_store.game = self.__game_factory.get_game()
        self.__game_store.game.start_singleplayer(self.__validator)

        Debug.print_playing_field(self.__game_store.game.playing_field_opponent)

        self.__game_store.game.show_message_place_ship(self.__game_store.game.ships_player[0], 0)
