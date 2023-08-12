from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side, GameState, Texts, Event
from models.images import Images
from models.position import Position
from models.validator import Validator
from store.gamestore import GameStore
from utils.messagehelper import MessageHelper
from views.mainview import MainView


class ShipHitEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game_store: GameStore, validator: Validator,
                 message_helper: MessageHelper, event_aggregator: EventAggregator) -> None:
        self.__main_view = main_view
        self.__game_store = game_store
        self.__validator = validator
        self.__message_helper = message_helper
        self.__event_aggregator = event_aggregator

    def execute(self, side: Side, pos: Position):
        hit_ship = self.__validator.get_ship_from_pos(side, pos)
        if pos in hit_ship.hit_positions:
            return
        hit_ship.hit_positions.append(pos)
        if self.__validator.is_ship_destroyed(hit_ship):
            messages = ["{0} sunk!".format(hit_ship.name)]
            self.__main_view.mark_ship_destroyed(side, hit_ship)
            hit_ship.is_destroyed = True
            ai_next = side == Side.RIGHT

            if self.__validator.are_all_ships_destroyed(side):
                messages.append("")
                if side == Side.RIGHT:
                    messages.append(Texts.PLAYER_WON)
                else:
                    if self.__game_store.game.game_state == GameState.SINGLEPLAYER:
                        messages.append(Texts.AI_WON)
                    elif self.__game_store.game.game_state == GameState.MULTIPLAYER:
                        messages.append(Texts.OPPONENT_WON)
                self.__main_view.set_status_label_text("")
                self.__game_store.game.game_state = GameState.GAME_OVER

            self.__message_helper.show(side, messages, ai_next, 0.1)
        else:
            self.__main_view.set_cell_image(side, pos, Images.HIT)
            if side == Side.RIGHT:
                self.__event_aggregator.publish(Event.AI_NEXT_MOVE_REQUESTED)
