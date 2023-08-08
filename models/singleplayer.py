import random

from models.enums import CellContent, Event, Side, GameState, Direction
from models.game import Game
from models.images import Images
from models.ship import Ship
from models.validator import Validator
from utils.debug import Debug
from utils.eventaggregator import EventAggregator
from utils.messagehelper import MessageHelper


class SinglePlayer:
    def __init__(
            self, event_aggregator: EventAggregator, game: Game, validator: Validator
    ) -> None:
        self.__event_aggregator = event_aggregator
        self.__game = game
        self.__validator = validator
        self.__fits_in_direction = Direction.NONE
        self.__ai_not_tried_positions = []
        self.__ai_hit_player_positions = []
        self.__ai_destroyed_player_ships = []

        for row in range(10):
            for column in range(10):
                self.__ai_not_tried_positions.append((row, column))

        self.num_placed_player_ships = 0

    def __get_possible_ship_positions(self, current_ship: Ship) -> list:
        validator = self.__validator
        positions = current_ship.positions

        if len(positions) == 1:
            return validator.get_adjacent_cells_free_nwse(Side.LEFT, positions[0][0], positions[0][1],
                                                          [positions[0]])

        if len(positions) == 2:
            if positions[0][0] == positions[1][0]:
                current_ship.orientation = Direction.HORIZONTAL
            else:
                current_ship.orientation = Direction.VERTICAL

        if current_ship.orientation == Direction.HORIZONTAL:
            return validator.get_adjacent_cells_free_we(Side.LEFT, current_ship, current_ship.positions)
        if current_ship.orientation == Direction.VERTICAL:
            return validator.get_adjacent_cells_free_ns(Side.LEFT, current_ship, current_ship.positions)

    def player_place_ship(self, row: int, column: int) -> None:
        game = self.__game
        validator = self.__validator
        current_ship: Ship = self.__game.ships_player[self.num_placed_player_ships]
        positions = current_ship.positions
        playing_field = self.__game.playing_field_player
        ships = self.__game.ships_player

        if playing_field[row][column] != CellContent.EMPTY:
            return

        if len(current_ship.positions) == 0:
            if validator.has_adjacent_cells_occupied(
                    Side.LEFT, row, column
            ):
                return
            fits_in_direction = validator.does_ship_fit_at_position(Side.LEFT, row, column, current_ship.length)
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
                MessageHelper.show(Side.LEFT, ["Game started!", "Make your first move..."])
                game.game_state = GameState.SINGLE_PLAYER
            else:
                self.show_message_place_ship(
                    ships[self.num_placed_player_ships], 0.2
                )

    def start(self) -> None:
        if self.__game.game_state == GameState.FIRST_RUN:
            self.__game.create_ships(Side.BOTH)
            self.__game.create_playing_field(Side.BOTH)
        else:
            self.__game.reset_playing_field(Side.BOTH)
            self.__game.reset_ships(Side.BOTH)
        self.__game.game_state = GameState.PLAYER_PLACING_SHIPS
        self.__game.whose_turn = Side.LEFT

        self.place_random_ships(Side.RIGHT)

    def place_random_ships(self, side: Side) -> None:
        from random import shuffle

        ships = []
        playing_field = []

        if side & Side.LEFT == Side.LEFT:
            ships = self.__game.ships_player
            playing_field = self.__game.playing_field_player
        if side & Side.RIGHT == Side.RIGHT:
            ships = self.__game.ships_opponent
            playing_field = self.__game.playing_field_opponent

        validator = self.__validator

        num_placed_ships = 0
        num_tries = 0
        max_tries = 100

        while num_placed_ships != len(ships) and num_tries < max_tries:
            num_placed_ships = 0
            if num_tries != 0:
                self.__game.reset_ships(side)
                self.__game.reset_playing_field(side)

                shuffle(ships)

            ship: Ship
            for ship in ships:
                is_ship_placed = False
                ship.orientation = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
                possible_rows = list(
                    range(10 if ship.orientation == Direction.HORIZONTAL else 10 - ship.length)
                )
                shuffle(possible_rows)
                possible_columns = list(
                    range(10 if ship.orientation == Direction.VERTICAL else 10 - ship.length)
                )
                shuffle(possible_columns)
                for row in possible_rows:
                    if is_ship_placed:
                        break
                    for column in possible_columns:
                        if is_ship_placed:
                            break
                        do_place = True
                        positions = []
                        for i in range(ship.length):
                            if ship.orientation == Direction.HORIZONTAL:
                                positions.append((row, column + i))
                            else:
                                positions.append((row + i, column))
                        for pos in positions:
                            if playing_field[pos[0]][
                                pos[1]] != CellContent.EMPTY or validator.has_adjacent_cells_occupied(
                                    side, pos[0], pos[1]
                            ):
                                do_place = False
                                break
                        if do_place:
                            for pos in positions:
                                playing_field[pos[0]][
                                    pos[1]
                                ] = CellContent.FILLED
                                ship.positions.append(pos)
                            is_ship_placed = True
                            num_placed_ships += 1
            num_tries += 1

        print("placed ships: {0}, tries: {1}".format(num_placed_ships, num_tries))

    def ai_make_move(self):
        ships = self.__game.ships_player
        random_pos = random.choice(self.__ai_not_tried_positions)

        self.__ai_not_tried_positions.remove(random_pos)
        for ship in ships:
            if random_pos in ship.positions:
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, random_pos[0], random_pos[1],
                                                Images.HIT)

                self.__event_aggregator.publish(Event.CHECK_IF_SHIP_DESTROYED, Side.LEFT, random_pos[0], random_pos[1])
                break

        self.__game.whose_turn = Side.LEFT

    @staticmethod
    def show_message_place_ship(ship: Ship, delay: float) -> None:
        message = "Place a {0} (length: {1})".format(ship.name, ship.length)
        MessageHelper.show(Side.LEFT, [message], delay)
