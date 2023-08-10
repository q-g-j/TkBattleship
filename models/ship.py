from models.enums import Orientation
from models.position import Position


class Ship:
    def __init__(self, name: str, length: int) -> None:
        self.name = name
        self.length = length
        self.orientation = Orientation.NONE
        self.positions: list[Position] = []
        self.hit_positions: list[Position] = []
        self.is_destroyed = False
