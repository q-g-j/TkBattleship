from random import shuffle, choice

from models.enums import *
from models.images import Images
from models.ship import Ship
from models.validator import Validator
from events.eventaggregator import EventAggregator
from utils.messagehelper import MessageHelper


class Game:
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

        self.ships_player = []
        self.ships_opponent = []
        self.playing_field_player = []
        self.playing_field_opponent = []

        self.game_state = GameState.FIRST_RUN
        self.whose_turn = Side.LEFT

        self.__fits_in_direction = Direction.NONE
        self.num_placed_player_ships = 0

    def create_ships(self, side: Side) -> None:
        for ship_type in ShipTypes:
            for _ in range(ship_type[2]):
                if side & Side.LEFT == Side.LEFT:
                    self.ships_player.append(Ship(ship_type[0], ship_type[1]))
                if side & Side.RIGHT == Side.RIGHT:
                    self.ships_opponent.append(Ship(ship_type[0], ship_type[1]))

    def create_playing_field(self, side: Side) -> None:
        for _ in range(10):
            playing_field_player_inner = []
            playing_field_opponent_inner = []
            for _ in range(10):
                if side & Side.LEFT == Side.LEFT:
                    playing_field_player_inner.append(CellContent.EMPTY)
                if side & Side.RIGHT == Side.RIGHT:
                    playing_field_opponent_inner.append(CellContent.EMPTY)
            if side & Side.LEFT == Side.LEFT:
                self.playing_field_player.append(playing_field_player_inner)
            if side & Side.RIGHT == Side.RIGHT:
                self.playing_field_opponent.append(playing_field_opponent_inner)

    def reset_ships(self, side: Side) -> None:
        if side & Side.LEFT == Side.LEFT:
            self.ships_player.clear()
        if side & Side.RIGHT == Side.RIGHT:
            self.ships_opponent.clear()

        self.create_ships(side)

    def reset_playing_field(self, side: Side) -> None:
        for row in range(10):
            for column in range(10):
                if side & Side.LEFT == Side.LEFT:
                    self.playing_field_player[row][column] = CellContent.EMPTY
                if side & Side.RIGHT == Side.RIGHT:
                    self.playing_field_opponent[row][column] = CellContent.EMPTY

    def player_place_ship(self, validator: Validator, row: int, column: int) -> None:
        current_ship: Ship = self.ships_player[self.num_placed_player_ships]
        positions = current_ship.positions
        playing_field = self.playing_field_player
        ships = self.ships_player

        if playing_field[row][column] != CellContent.EMPTY:
            return

        if len(current_ship.positions) == 0:
            if validator.has_adjacent_cells_occupied(Side.LEFT, row, column):
                return
            fits_in_direction = validator.does_ship_fit_at_position(Side.LEFT, row, column,
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

            possible_positions = validator.get_possible_ship_positions(current_ship)
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
                self.game_state = GameState.SINGLE_PLAYER
            else:
                self.show_message_place_ship(
                    ships[self.num_placed_player_ships], 0.2
                )

    def place_random_ships(self, validator: Validator, side: Side) -> None:
        ships = []
        playing_field = []

        if side & Side.LEFT == Side.LEFT:
            ships = self.ships_player
            playing_field = self.playing_field_player
        if side & Side.RIGHT == Side.RIGHT:
            ships = self.ships_opponent
            playing_field = self.playing_field_opponent

        num_placed_ships = 0
        num_tries = 0
        max_tries = 100

        while num_placed_ships != len(ships) and num_tries < max_tries:
            num_placed_ships = 0
            if num_tries != 0:
                self.reset_ships(side)
                self.reset_playing_field(side)

                shuffle(ships)

            ship: Ship
            for ship in ships:
                is_ship_placed = False
                ship.orientation = choice([Direction.HORIZONTAL, Direction.VERTICAL])
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
                            if playing_field[pos[0]][pos[1]] != CellContent.EMPTY \
                                    or validator.has_adjacent_cells_occupied(side, pos[0], pos[1]):
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

        # print("placed ships: {0}, tries: {1}".format(num_placed_ships, num_tries))

    @staticmethod
    def show_message_place_ship(ship: Ship, delay: float) -> None:
        message = "Place a {0} (length: {1})".format(ship.name, ship.length)
        MessageHelper.show(Side.LEFT, [message], delay)
