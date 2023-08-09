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

        self.__fits_in_direction = Direction.NONE
        self.__ai_not_tried_positions = []
        self.__ai_hit_player_positions = []
        self.__ai_destroyed_player_ships = []

        self.num_placed_player_ships = 0

    def __get_possible_ship_positions(self, current_ship: Ship) -> list:
        positions = current_ship.positions

        if len(positions) == 1:
            return self.__validator.get_adjacent_cells_free_nwse(Side.LEFT, positions[0][0], positions[0][1],
                                                                 [positions[0]])

        if len(positions) == 2:
            if positions[0][0] == positions[1][0]:
                current_ship.orientation = Direction.HORIZONTAL
            else:
                current_ship.orientation = Direction.VERTICAL

        if current_ship.orientation == Direction.HORIZONTAL:
            return self.__validator.get_adjacent_cells_free_we(Side.LEFT, current_ship, current_ship.positions)
        if current_ship.orientation == Direction.VERTICAL:
            return self.__validator.get_adjacent_cells_free_ns(Side.LEFT, current_ship, current_ship.positions)

    def player_place_ship(self, row: int, column: int) -> None:
        game = self.__game
        current_ship: Ship = self.__game.ships_player[self.num_placed_player_ships]
        positions = current_ship.positions
        playing_field = self.__game.playing_field_player
        ships = self.__game.ships_player

        if playing_field[row][column] != CellContent.EMPTY:
            return

        if len(current_ship.positions) == 0:
            if self.__validator.has_adjacent_cells_occupied(Side.LEFT, row, column):
                return
            fits_in_direction = self.__validator.does_ship_fit_at_position(Side.LEFT, row, column,
                                                                           current_ship.length)
            if fits_in_direction == Direction.NONE:
                self.__fits_in_direction = Direction.NONE
                return
            else:
                self.__fits_in_direction = fits_in_direction
        if len(positions) >= 1:
            if self.__fits_in_direction == Direction.HORIZONTAL and row != positions[0][0]:
                return
            if self.__fits_in_direction == Direction.VERTICAL and column != positions[0][1]:
                return

            possible_positions = self.__get_possible_ship_positions(current_ship)
            if (row, column) not in possible_positions:
                return

        playing_field[row][column] = CellContent.FILLED
        self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, row, column, Images.UNDAMAGED_GREEN)

        positions.append((row, column))
        if len(positions) == current_ship.length:
            for pos in positions:
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, pos[0], pos[1], Images.UNDAMAGED)
            self.num_placed_player_ships += 1

            if self.num_placed_player_ships == len(ships):
                self.__event_aggregator.publish(Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED, False)
                MessageHelper.show(Side.LEFT, ["Game started!", "Make your first move..."])
                game.game_state = GameState.SINGLE_PLAYER
            else:
                self.show_message_place_ship(
                    ships[self.num_placed_player_ships], 0.2
                )

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

        self.num_placed_player_ships = 0

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

    @staticmethod
    def show_message_place_ship(ship: Ship, delay: float) -> None:
        message = "Place a {0} (length: {1})".format(ship.name, ship.length)
        MessageHelper.show(Side.LEFT, [message], delay)
