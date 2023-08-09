from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.enums import Side, GameState
from models.game import Game
from models.ship import Ship
from models.validator import Validator
from utils.messagehelper import MessageHelper
from views.mainview import MainView


class CheckShipDestroyedRequestedEventHandler(EventHandlerBase):
    def __init__(self, main_view: MainView, game: Game, validator: Validator) -> None:
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator

    def execute(self, side: Side, row: int, column: int):
        ship: Ship = self.__validator.get_destroyed_ship(side, row, column)
        if ship is not None:
            self.__main_view.mark_ship_destroyed(side, ship)
            messages = ["{0} sunk!".format(ship.name)]
            if self.__validator.are_all_ships_destroyed(side):
                self.__game.game_state = GameState.GAME_OVER
                messages.append("")
                if side == Side.LEFT:
                    messages.append("Your opponent has won")
                else:
                    messages.append("You have won")

            MessageHelper.show(side, messages, 0.3)
