from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side, GameState
from models.game import Game
from models.images import Images
from models.singleplayer import SinglePlayer
from models.validator import Validator
from views.mainview import MainView


class CellClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game: Game, validator: Validator, singleplayer: SinglePlayer) -> None:
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator
        self.__singleplayer = singleplayer

    def execute(self, side: Side, row: int, column: int):
        # close the menu if open and RETURN:
        if self.__main_view.is_menu_open:
            if self.__game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()
                return

        # close the messagebox if open and RETURN:
        if self.__main_view.is_messagebox_open:
            self.__main_view.close_messagebox()
            return

        # don't allow cell clicks on first run and game over:
        if self.__game.game_state in (
                GameState.FIRST_RUN,
                GameState.GAME_OVER,
        ):
            return

        # when game has started don't allow to click on the left side:
        if self.__game.game_state in (GameState.SINGLE_PLAYER, GameState.MULTIPLAYER) and side == Side.LEFT:
            return

        # if player is currently placing ships:
        if self.__game.game_state == GameState.PLAYER_PLACING_SHIPS:

            # don't allow clicks on the right side:
            if side == Side.RIGHT:
                return

            # go to function Singleplayer.player_place_ship(), then RETURN:
            if side == Side.LEFT:
                self.__singleplayer.player_place_ship(row, column)
                return

        # finally:
        # if cell is filled, mark it as hit and check if ship is destroyed:
        if not self.__validator.is_cell_empty(side, row, column):
            self.__main_view.set_cell_image(side, row, column, Images.HIT)
            self.__validator.get_destroyed_ship(Side.RIGHT, row, column)

        # singleplayer mode: let the AI make it's move:
        if self.__game.whose_turn == Side.LEFT and self.__game.game_state == GameState.SINGLE_PLAYER:
            self.__singleplayer.ai_make_move()
