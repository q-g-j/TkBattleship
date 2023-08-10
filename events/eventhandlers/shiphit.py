from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side, GameState, Texts
from models.game import Game
from models.images import Images
from models.position import Position
from models.ship import Ship
from models.validator import Validator
from utils.messagehelper import MessageHelper
from views.main import Main


class ShipHitEventHandler(EventHandlerBase):
    def __init__(self, main_view: Main, game: Game, validator: Validator) -> None:
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator

    def execute(self, side: Side, pos: Position, game_state: GameState):
        hit_ship = self.__validator.get_ship_from_pos(side, pos)
        if pos in hit_ship.hit_positions:
            return
        hit_ship.hit_positions.append(pos)
        if self.__validator.is_ship_destroyed(hit_ship):
            messages = ["{0} sunk!".format(hit_ship.name)]
            self.__main_view.mark_ship_destroyed(side, hit_ship)
            hit_ship.is_destroyed = True
            if self.__validator.are_all_ships_destroyed(side):
                self.__game.game_state = GameState.GAME_OVER
                messages.append("")
                if side == Side.RIGHT:
                    messages.append(Texts.PLAYER_WON)
                else:
                    if game_state == GameState.SINGLEPLAYER:
                        messages.append(Texts.AI_WON)
                    elif game_state == GameState.MULTIPLAYER:
                        messages.append(Texts.OPPONENT_WON)
                self.__main_view.set_status_label_text("")
            MessageHelper.show(side, messages, 0.1)
        else:
            self.__main_view.set_cell_image(side, pos, Images.HIT)
