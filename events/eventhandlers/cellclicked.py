from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side, GameState, Event, Texts
from models.game import Game
from models.position import Position
from models.singleplayer import SinglePlayer
from models.validator import Validator
from utils.sleep import threaded_sleep
from views.main import Main


class CellClickedEventHandler(EventHandlerBase):
    def __init__(
            self,
            main_view: Main,
            game: Game,
            validator: Validator,
            singleplayer: SinglePlayer,
            event_aggregator: EventAggregator,
    ) -> None:
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator
        self.__singleplayer = singleplayer
        self.__event_aggregator = event_aggregator

    def execute(self, side: Side, pos: Position):
        # close the menu if open and RETURN:
        if self.__main_view.is_menu_open:
            if self.__game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()
                return

        # close the messagebox if open and RETURN:
        if (
                self.__main_view.is_messagebox_open
                and not self.__game.game_state == GameState.GAME_OVER
        ):
            self.__main_view.close_messagebox()
            return

        # don't allow cell clicks on first run and game over:
        if self.__game.game_state in (
                GameState.FIRST_RUN,
                GameState.GAME_OVER,
        ):
            return

        # when game has started don't allow to click on the left side:
        if (
                self.__game.game_state in (GameState.SINGLEPLAYER, GameState.MULTIPLAYER)
                and side == Side.LEFT
        ):
            return

        # don't allow clicks on the right side, when it's the right player's turn:
        if (
                self.__game.game_state in (GameState.SINGLEPLAYER, GameState.MULTIPLAYER)
                and side == Side.RIGHT
                and self.__game.whose_turn == Side.RIGHT
        ):
            return

        # if player is currently placing ships:
        if self.__game.game_state == GameState.PLAYER_PLACING_SHIPS:
            # don't allow clicks on the right side:
            if side == Side.RIGHT:
                return

            # go to function Singleplayer.player_place_ship(), then RETURN:
            if side == Side.LEFT:
                self.__game.player_place_ship(self.__validator, pos)
                return

        # finally:
        # if cell is filled, mark it as hit and check if ship is destroyed:
        if not self.__validator.is_cell_empty(side, pos):
            self.__event_aggregator.publish(Event.SHIP_HIT, side, pos, self.__game.game_state)

        # singleplayer mode: let the AI make it's move:
        if (
                self.__game.whose_turn == Side.LEFT
                and self.__game.game_state == GameState.SINGLEPLAYER
        ):
            self.__game.whose_turn = Side.RIGHT
            self.__main_view.set_status_label_text(Texts.STATUS_LABEL_AI_TURN)
            threaded_sleep(lambda: self.__singleplayer.ai_make_move(), 0.5)
