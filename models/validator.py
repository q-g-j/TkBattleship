from models.enums import Side, CellContent, Direction
from models.ship import Ship


class Validator:
    def __init__(self, playing_field_player: list, playing_field_opponent: list, ships_player: list, ships_opponent):
        self.playing_field_player = playing_field_player
        self.playing_field_opponent = playing_field_opponent
        self.ships_player = ships_player
        self.ships_opponent = ships_opponent

    def has_adjacent_cells_occupied(
            self,
            side: Side,
            row: int,
            column: int,
            except_positions: list = None,
    ) -> bool:

        if not except_positions:
            except_positions = []
        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if 0 <= r <= 9 and 0 <= c <= 9:
                    if (r, c) not in except_positions:
                        if playing_field[r][c] != CellContent.EMPTY:
                            return True
        return False

    def get_adjacent_cells_free_ns(self,
                                   side: Side,
                                   ship: Ship,
                                   _except_positions: list = None
                                   ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent

        min_position = ship.positions[0]
        max_position = ship.positions[0]

        for pos in ship.positions:
            if pos[0] < min_position[0]:
                min_position = pos
            elif pos[0] > max_position[0]:
                max_position = pos

        for pos in [(min_position[0] - 1, min_position[1]), (max_position[0] + 1, max_position[1])]:
            if 0 <= pos[0] <= 9:
                if playing_field[pos[0]][pos[1]] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(side, pos[0], pos[1], _except_positions):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def get_adjacent_cells_free_we(self,
                                   side: Side,
                                   ship: Ship,
                                   except_positions: list = None
                                   ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent

        min_position = ship.positions[0]
        max_position = ship.positions[0]

        for pos in ship.positions:
            if pos[1] < min_position[1]:
                min_position = pos
            elif pos[1] > max_position[1]:
                max_position = pos

        for pos in [(min_position[0], min_position[1] - 1), (max_position[0], max_position[1] + 1)]:
            if 0 <= pos[1] <= 9:
                if playing_field[pos[0]][pos[1]] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(side, pos[0], pos[1], except_positions):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def get_adjacent_cells_free_nwse(self,
                                     side: Side,
                                     row: int,
                                     column: int,
                                     except_positions: list = None
                                     ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent

        for pos in [(row - 1, column), (row, column - 1), (row + 1, column), (row, column + 1)]:
            if 0 <= pos[0] <= 9 and 0 <= pos[1] <= 9:
                if playing_field[pos[0]][pos[1]] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(side, pos[0], pos[1], except_positions):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def does_ship_fit_at_position(self, side: Side, row: int, column: int, length: int) -> Direction:
        """
        Checks wether a ship of a given length fits horizontally or vertically
        if starting at the requested coordinates
        :param side: left or right side of the playing field
        :param row: the row of the requested position
        :param column: the column of the requested position
        :param length: the length of the ship to try
        :return: Enum Direction (none, horizontal, vertical, both)
        """
        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent

        # if there are ships in sight, adjust the boundaries of the current row or column accordingly:
        top, left = 0, 0
        bottom, right = 9, 9

        for a in range(row, 10):
            if playing_field[a][column] != CellContent.EMPTY:
                bottom = a - 1
                break

        for a in reversed(range(0, row)):
            if playing_field[a][column] != CellContent.EMPTY:
                top = a + 1
                break

        for a in range(column, 10):
            if playing_field[row][a] != CellContent.EMPTY:
                right = a - 1
                break

        for a in reversed(range(0, column)):
            if playing_field[row][a] != CellContent.EMPTY:
                left = a + 1
                break

        def check_horizontally() -> bool:
            if right - left < length:
                return False

            if column + length <= right + 1:
                first = []
                for c in range(column, column + length):
                    if not self.has_adjacent_cells_occupied(side, row, c):
                        first.append((row, c))
                if len(first) == length:
                    return True

                for i in range(1, length):
                    if column - i < left:
                        break
                    remaining = []
                    for c2 in range(column - i, column + length - i):
                        if not self.has_adjacent_cells_occupied(side, row, c2):
                            remaining.append((row, c2))
                    if len(remaining) == length:
                        return True

            else:
                first = []
                for c in range(column - length + 1, column + 1):
                    if not self.has_adjacent_cells_occupied(side, row, c):
                        first.append((row, c))
                if len(first) == length:
                    return True
                for i in range(1, length):
                    if column + i > right:
                        break
                    remaining = []
                    for c2 in range(column - length + 1 + i, column + i + 1):
                        if not self.has_adjacent_cells_occupied(side, row, c2):
                            remaining.append((row, c2))
                    if len(remaining) == length:
                        return True

        def check_vertically() -> bool:
            if bottom - top < length:
                return False

            if row + length <= bottom + 1:
                first = []
                for r in range(row, row + length):
                    if not self.has_adjacent_cells_occupied(side, r, column):
                        first.append((r, column))
                if len(first) == length:
                    return True

                for i in range(1, length):
                    if row - i < top:
                        break
                    remaining = []
                    for r2 in range(row - i, row + length - i):
                        if not self.has_adjacent_cells_occupied(side, r2, column):
                            remaining.append((r2, column))
                    if len(remaining) == length:
                        return True

            else:
                first = []
                for r in range(row - length + 1, row + 1):
                    if not self.has_adjacent_cells_occupied(side, r, column):
                        first.append((r, column))
                if len(first) == length:
                    return True
                for i in range(1, length):
                    if row + i > bottom:
                        break
                    remaining = []
                    for r2 in range(row - length + 1 + i, row + i + 1):
                        if not self.has_adjacent_cells_occupied(side, r2, column):
                            remaining.append((r2, column))
                    if len(remaining) == length:
                        return True

        fits_horizontally = check_horizontally()
        fits_vertically = check_vertically()

        if fits_horizontally and fits_vertically:
            return Direction.BOTH
        elif fits_horizontally:
            return Direction.HORIZONTAL
        elif fits_vertically:
            return Direction.VERTICAL

        return Direction.NONE

    def are_all_ships_destroyed(self, side: Side) -> bool:
        if side == Side.LEFT:
            ships = self.ships_player
        else:
            ships = self.ships_opponent
        num_destroyed = 0

        ship: Ship
        for ship in ships:
            if ship.is_destroyed:
                num_destroyed += 1
        return True if num_destroyed == len(ships) else False

    def is_cell_empty(self, side: Side, row: int, column: int) -> bool:
        if side == Side.LEFT:
            playing_field = self.playing_field_player
        else:
            playing_field = self.playing_field_opponent
        if playing_field[row][column] == CellContent.EMPTY:
            return True
        return False

    def get_destroyed_ship(
            self, side: Side, row: int, column: int
    ) -> Ship | None:
        if side == Side.LEFT:
            ships = self.ships_player
        else:
            ships = self.ships_opponent

        ship: Ship
        for ship in ships:
            pos = (row, column)
            if pos in ship.positions:
                if pos not in ship.hit_positions:
                    ship.hit_positions.append(pos)
                if len(ship.hit_positions) == ship.length:
                    destroyed_positions = []
                    for hit_pos in ship.positions:
                        destroyed_positions.append(hit_pos)
                    ship.is_destroyed = True
                    return ship
        return None
