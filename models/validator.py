from models.enums import Side, CellContent, Orientation
from models.position import Position
from models.ship import Ship

from services.injector import inject

from models.game import Game


@inject(Game)
class Validator:
    def __init__(self, game):
        self.__game = game

    def has_adjacent_cells_occupied(
            self,
            side: Side,
            pos: Position,
            except_positions: list = None,
    ) -> bool:
        if not except_positions:
            except_positions: list[Position] = []
        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent
        for r in range(pos.row - 1, pos.row + 2):
            for c in range(pos.col - 1, pos.col + 2):
                if 0 <= r <= 9 and 0 <= c <= 9:
                    adj_pos = Position(r, c)
                    if r == pos.row and c == pos.col:
                        continue
                    if adj_pos not in except_positions:
                        if playing_field[r][c] != CellContent.EMPTY:
                            return True
        return False

    @staticmethod
    def get_adjacent_positions_nwse(pos: Position, from_positions: list[Position] | None = None) -> list[Position]:
        adjacent_positions: list[Position] = []

        for r in range(pos.row - 1, pos.row + 2):
            for c in range(pos.col - 1, pos.col + 2):
                if 0 <= r <= 9 and 0 <= c <= 9:
                    if r == pos.row and c == pos.col:
                        continue
                    adj_pos = Position(r, c)
                    if adj_pos not in adjacent_positions and (from_positions is None or adj_pos in from_positions):
                        adjacent_positions.append(Position(r, c))
        return adjacent_positions

    def get_adjacent_cells_free_ns(
            self, side: Side, ship: Ship, except_positions: list = None
    ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent

        min_position = ship.positions[0]
        max_position = ship.positions[0]

        for pos in ship.positions:
            if pos.row < min_position.row:
                min_position = pos
            elif pos.row > max_position.row:
                max_position = pos

        for pos in [
            Position(min_position.row - 1, min_position.col),
            Position(max_position.row + 1, max_position.col),
        ]:
            if 0 <= pos.row <= 9:
                if playing_field[pos.row][pos.col] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(
                            side, pos, except_positions
                    ):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def get_adjacent_cells_free_we(
            self, side: Side, ship: Ship, except_positions: list = None
    ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent

        min_position = ship.positions[0]
        max_position = ship.positions[0]

        for pos in ship.positions:
            if pos.col < min_position.col:
                min_position = pos
            elif pos.col > max_position.col:
                max_position = pos

        for pos in [
            Position(min_position.row, min_position.col - 1),
            Position(max_position.row, max_position.col + 1),
        ]:
            if 0 <= pos.col <= 9:
                if playing_field[pos.row][pos.col] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(
                            side, pos, except_positions
                    ):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def get_adjacent_cells_free_nwse(
            self, side: Side, pos: Position, except_positions: list = None
    ) -> list:
        adjacent_positions = []

        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent

        for pos in [
            Position(pos.row - 1, pos.col),
            Position(pos.row, pos.col - 1),
            Position(pos.row + 1, pos.col),
            Position(pos.row, pos.col + 1),
        ]:
            if 0 <= pos.row <= 9 and 0 <= pos.col <= 9:
                if playing_field[pos.row][pos.col] == CellContent.EMPTY:
                    if not self.has_adjacent_cells_occupied(
                            side, pos, except_positions
                    ):
                        adjacent_positions.append(pos)

        return adjacent_positions

    def does_ship_fit_at_position(
            self, side: Side, pos: Position, length: int
    ) -> Orientation:
        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent

        # if there are ships in sight, adjust the boundaries of the current row or column accordingly:
        top, left = 0, 0
        bottom, right = 9, 9

        for a in range(pos.row, 10):
            if playing_field[a][pos.col] != CellContent.EMPTY:
                bottom = a - 1
                break

        for a in reversed(range(0, pos.row)):
            if playing_field[a][pos.col] != CellContent.EMPTY:
                top = a + 1
                break

        for a in range(pos.col, 10):
            if playing_field[pos.row][a] != CellContent.EMPTY:
                right = a - 1
                break

        for a in reversed(range(0, pos.col)):
            if playing_field[pos.row][a] != CellContent.EMPTY:
                left = a + 1
                break

        def check_horizontally() -> bool:
            if right - left < length:
                return False

            if pos.col + length <= right + 1:
                first: list[Position] = []
                for c in range(pos.col, pos.col + length):
                    if not self.has_adjacent_cells_occupied(side, Position(pos.row, c)):
                        first.append(Position(pos.row, c))
                if len(first) == length:
                    return True

                for i in range(1, length):
                    if pos.col - i < left:
                        break
                    remaining: list[Position] = []
                    for c2 in range(pos.col - i, pos.col + length - i):
                        if not self.has_adjacent_cells_occupied(
                                side, Position(pos.row, c2)
                        ):
                            remaining.append(Position(pos.row, c2))
                    if len(remaining) == length:
                        return True

            else:
                first: list[Position] = []
                for c in range(pos.col - length + 1, pos.col + 1):
                    if not self.has_adjacent_cells_occupied(side, Position(pos.row, c)):
                        first.append(Position(pos.row, c))
                if len(first) == length:
                    return True
                for i in range(1, length):
                    if pos.col + i > right:
                        break
                    remaining: list[Position] = []
                    for c2 in range(pos.col - length + 1 + i, pos.col + i + 1):
                        if not self.has_adjacent_cells_occupied(
                                side, Position(pos.row, c2)
                        ):
                            remaining.append(Position(pos.row, c2))
                    if len(remaining) == length:
                        return True

        def check_vertically() -> bool:
            if bottom - top < length:
                return False

            if pos.row + length <= bottom + 1:
                first: list[Position] = []
                for r in range(pos.row, pos.row + length):
                    if not self.has_adjacent_cells_occupied(side, Position(r, pos.col)):
                        first.append(Position(r, pos.col))
                if len(first) == length:
                    return True

                for i in range(1, length):
                    if pos.row - i < top:
                        break
                    remaining: list[Position] = []
                    for r2 in range(pos.row - i, pos.row + length - i):
                        if not self.has_adjacent_cells_occupied(
                                side, Position(r2, pos.col)
                        ):
                            remaining.append(Position(r2, pos.col))
                    if len(remaining) == length:
                        return True

            else:
                first: list[Position] = []
                for r in range(pos.row - length + 1, pos.row + 1):
                    if not self.has_adjacent_cells_occupied(side, Position(r, pos.col)):
                        first.append(Position(r, pos.col))
                if len(first) == length:
                    return True
                for i in range(1, length):
                    if pos.row + i > bottom:
                        break
                    remaining: list[Position] = []
                    for r2 in range(pos.row - length + 1 + i, pos.row + i + 1):
                        if not self.has_adjacent_cells_occupied(
                                side, Position(r2, pos.col)
                        ):
                            remaining.append(Position(r2, pos.col))
                    if len(remaining) == length:
                        return True

        fits_horizontally = check_horizontally()
        fits_vertically = check_vertically()

        if fits_horizontally and fits_vertically:
            return Orientation.BOTH
        elif fits_horizontally:
            return Orientation.HORIZONTAL
        elif fits_vertically:
            return Orientation.VERTICAL

        return Orientation.NONE

    def are_all_ships_destroyed(self, side: Side) -> bool:
        if side == Side.LEFT:
            ships = self.__game.ships_player
        else:
            ships = self.__game.ships_opponent
        num_destroyed = 0

        ship: Ship
        for ship in ships:
            if ship.is_destroyed:
                num_destroyed += 1
        return True if num_destroyed == len(ships) else False

    def is_cell_empty(self, side: Side, pos: Position) -> bool:
        if side == Side.LEFT:
            playing_field = self.__game.playing_field_player
        else:
            playing_field = self.__game.playing_field_opponent
        if playing_field[pos.row][pos.col] == CellContent.EMPTY:
            return True
        return False

    def get_ship_from_pos(self, side: Side, pos: Position) -> Ship | None:
        if side == Side.LEFT:
            ships = self.__game.ships_player
        else:
            ships = self.__game.ships_opponent

        ship: Ship
        for ship in ships:
            if pos in ship.positions:
                return ship

        return None

    @staticmethod
    def is_ship_destroyed(ship: Ship) -> bool:
        return len(ship.hit_positions) == ship.length

    def is_ship_destroyed_at_position(self, side: Side, pos: Position) -> bool:
        ship = self.get_ship_from_pos(side, pos)
        if ship is not None:
            return Validator.is_ship_destroyed(ship)

        return False

    def get_destroyed_ship(self, side: Side, pos: Position) -> Ship | None:
        if side == Side.LEFT:
            ships = self.__game.ships_player
        else:
            ships = self.__game.ships_opponent

        ship: Ship

        for ship in ships:
            if pos in ship.positions:
                if len(ship.hit_positions) == ship.length:
                    ship.is_destroyed = True
                    return ship
        return None

    @staticmethod
    def get_ship_orientation_from_positions(pos1: Position, pos2: Position) -> Orientation:
        if pos1.row == pos2.row:
            return Orientation.HORIZONTAL
        else:
            return Orientation.VERTICAL

    def get_possible_ship_positions(self, current_ship: Ship) -> list:
        positions = current_ship.positions

        if len(positions) == 1:
            return self.get_adjacent_cells_free_nwse(
                Side.LEFT, Position(positions[0].row, positions[0].col), [positions[0]]
            )

        if len(positions) == 2:
            current_ship.orientation = self.get_ship_orientation_from_positions(positions[0], positions[1])

        if current_ship.orientation == Orientation.HORIZONTAL:
            return self.get_adjacent_cells_free_we(
                Side.LEFT, current_ship, current_ship.positions
            )
        if current_ship.orientation == Orientation.VERTICAL:
            return self.get_adjacent_cells_free_ns(
                Side.LEFT, current_ship, current_ship.positions
            )
