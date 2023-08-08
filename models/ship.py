from models.enums import Direction


class Ship:
    def __init__(self, name: str, length: int) -> None:
        self.name = name
        self.length = length
        self.orientation = Direction.NONE
        self.positions = []
        self.hit_positions = []
        self.is_destroyed = False
