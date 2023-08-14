from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import GameState, Side, Texts
from views.images import Images
from models.validator import Validator
from store.gamestore import GameStore
from views.mainview import MainView


class RandomShipsButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game_store: GameStore, validator: Validator) -> None:
        self.__main_view = main_view
        self.__game_store = game_store
        self.__validator = validator

    def execute(self):
        self.__main_view.close_messagebox()
        self.__main_view.clear_cells(Side.LEFT)
        self.__game_store.game.reset_ships(Side.LEFT)
        self.__game_store.game.reset_playing_field(Side.LEFT)
        self.__game_store.game.num_placed_player_ships = 0

        self.__game_store.game.place_random_ships(self.__validator, Side.LEFT)

        for ship in self.__game_store.game.ships_player:
            for pos in ship.positions:
                self.__main_view.set_cell_image(Side.LEFT, pos, Images.UNDAMAGED)
        self.__game_store.game.game_state = GameState.SINGLEPLAYER

        self.__main_view.change_random_ships_button_visibility(False)
        self.__main_view.set_status_label_text(Texts.STATUS_LABEL_PLAYER_TURN)
