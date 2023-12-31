from models.enums import Side, GameState, Event
from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.position import Position
from models.validator import Validator
from store.gamestore import GameStore
from utils.sleep import threaded_sleep
from views.images import Images
from views.mainview import MainView


class CellClickedEventHandler(EventHandlerBase):
    def __init__(
        self,
        main_view: MainView,
        game_store: GameStore,
        validator: Validator,
        event_aggregator: EventAggregator,
    ) -> None:
        self.__main_view = main_view
        self.__game_store = game_store
        self.__validator = validator
        self.__event_aggregator = event_aggregator

    def execute(self, side: Side, pos: Position) -> None:
        if self.__game_store.game is None:
            return

        # close the menu if open and RETURN:
        if self.__main_view.is_menu_open:
            if self.__game_store.game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()
                return

        # close the messagebox if open and RETURN:
        if self.__main_view.is_messagebox_open and not self.__game_store.game.game_state == GameState.GAME_OVER:
            self.__main_view.close_messagebox()
            return

        # don't allow cell clicks on first run and game over:
        if self.__game_store.game.game_state in (
            GameState.FIRST_RUN,
            GameState.GAME_OVER,
        ):
            return

        # when game has started don't allow to click on the left side:
        if self.__game_store.game.game_state in (GameState.SINGLEPLAYER, GameState.MULTIPLAYER) and (side == Side.LEFT):
            return

        # don't allow clicks on the right side, when it's the right player's turn:
        if (
            self.__game_store.game.game_state in (GameState.SINGLEPLAYER, GameState.MULTIPLAYER)
            and side == Side.RIGHT
            and self.__game_store.game.whose_turn == Side.RIGHT
        ):
            return

        # if player is currently placing ships:
        if self.__game_store.game.game_state == GameState.PLAYER_PLACING_SHIPS:
            # don't allow clicks on the right side:
            if side == Side.RIGHT:
                return

            # go to function Singleplayer.player_place_ship(), then RETURN:
            if side == Side.LEFT:
                self.__game_store.game.player_place_ship(self.__validator, pos)
                return

        # finally:
        # if cell is filled, mark it as hit and check if ship is destroyed:
        if self.__game_store.game.whose_turn == Side.LEFT:
            if self.__validator.is_position_hit(Side.RIGHT, pos):
                return

            self.__game_store.game.whose_turn = Side.RIGHT

            if not self.__validator.is_cell_empty(side, pos):
                self.__event_aggregator.publish(Event.SHIP_HIT, side, pos)

            else:
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, side, pos, Images.SPLASH)

                def clear_image_and_make_ai_move():
                    self.__event_aggregator.publish(Event.CELL_IMAGE_SET, side, pos, Images.EMPTY)
                    self.__event_aggregator.publish(Event.AI_NEXT_MOVE_REQUESTED)

                # singleplayer mode: let the AI make it's move:
                if (
                    self.__game_store.game.game_state == GameState.SINGLEPLAYER
                    and not self.__main_view.is_messagebox_open
                ):
                    threaded_sleep(clear_image_and_make_ai_move, 0.5)
