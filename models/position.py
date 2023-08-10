from __future__ import annotations
from models.enums import NotationColumns


class Position:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.col = column

    def __eq__(self, other: Position):
        return True if self.row == other.row and self.col == other.col else False

    def __str__(self):
        return f"({NotationColumns[self.col + 1]}, {self.row + 1})"

    def __repr__(self):
        return f"({NotationColumns[self.col + 1]}, {self.row + 1})"

    def is_left_of(self, other: Position) -> bool:
        return True if self.col < other.col else False

    def is_top_of(self, other: Position) -> bool:
        return True if self.row < other.row else False

    @staticmethod
    def get_left_and_right(pos1: Position, pos2: Position) -> tuple[Position, Position]:
        if pos1.is_left_of(pos2):
            left_pos = pos1
            right_pos = pos2
        else:
            left_pos = pos2
            right_pos = pos1

        return left_pos, right_pos

    @staticmethod
    def get_top_and_bottom(pos1: Position, pos2: Position) -> tuple[Position, Position]:
        if pos1.is_top_of(pos2):
            top_pos = pos1
            bottom_pos = pos2
        else:
            top_pos = pos2
            bottom_pos = pos1

        return top_pos, bottom_pos
