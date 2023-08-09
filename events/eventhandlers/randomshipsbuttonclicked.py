from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import GameState, Side
from models.game import Game
from models.images import Images
from models.singleplayer import SinglePlayer
from models.validator import Validator
from views.mainview import MainView


class RandomShipsButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game: Game, validator: Validator, singleplayer: SinglePlayer) -> None:
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator
        self.__singleplayer = singleplayer

    def execute(self):
        self.__main_view.close_messagebox()
        self.__main_view.clear_cells(Side.LEFT)
        self.__game.reset_ships(Side.LEFT)
        self.__game.reset_playing_field(Side.LEFT)
        self.__game.num_placed_player_ships = 0

        self.__game.place_random_ships(self.__validator, Side.LEFT)

        for ship in self.__game.ships_player:
            for pos in ship.positions:
                self.__main_view.set_cell_image(Side.LEFT, pos, Images.UNDAMAGED)
        self.__game.game_state = GameState.SINGLE_PLAYER

        self.__main_view.change_random_ships_button_visibility(False)
