from random import shuffle, choice

from models.enums import *
from models.ship import Ship
from models.validator import Validator
from events.eventaggregator import EventAggregator


class Game:
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

        self.ships_player = []
        self.ships_opponent = []
        self.playing_field_player = []
        self.playing_field_opponent = []

        self.game_state = GameState.FIRST_RUN
        self.whose_turn = Side.LEFT

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
