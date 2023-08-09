import random

from models.enums import CellContent, Event, Side, GameState, Direction
from models.game import Game
from models.images import Images
from models.ship import Ship
from models.validator import Validator
# from utils.debug import Debug
from events.eventaggregator import EventAggregator
from utils.messagehelper import MessageHelper


class SinglePlayer:
    def __init__(self, event_aggregator: EventAggregator, game: Game, validator: Validator) -> None:
        self.__event_aggregator = event_aggregator
        self.__game = game
        self.__validator = validator
        self.__ai_not_tried_positions = []
        self.__ai_hit_player_positions = []
        self.__ai_destroyed_player_ships = []

    def ai_make_move(self):
        ships = self.__game.ships_player
        random_pos = random.choice(self.__ai_not_tried_positions)

        self.__ai_not_tried_positions.remove(random_pos)
        for ship in ships:
            if random_pos in ship.positions:
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, random_pos[0], random_pos[1],
                                                Images.HIT)

                self.__event_aggregator.publish(Event.CHECK_SHIP_DESTROYED_REQUESTED, Side.LEFT, random_pos[0], random_pos[1])
                break

        self.__game.whose_turn = Side.LEFT

    def start(self) -> None:
        self.__ai_not_tried_positions = []
        self.__ai_hit_player_positions = []
        self.__ai_destroyed_player_ships = []

        for row in range(10):
            for column in range(10):
                self.__ai_not_tried_positions.append((row, column))

        self.__game.num_placed_player_ships = 0

        if self.__game.game_state == GameState.FIRST_RUN:
            self.__game.create_ships(Side.BOTH)
            self.__game.create_playing_field(Side.BOTH)
        else:
            self.__game.reset_playing_field(Side.BOTH)
            self.__game.reset_ships(Side.BOTH)
        self.__game.game_state = GameState.PLAYER_PLACING_SHIPS
        self.__game.whose_turn = Side.LEFT

        self.__event_aggregator.publish(Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED, True)

        self.__game.place_random_ships(self.__validator, Side.RIGHT)
