from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.game import Game


class GameStore:
    def __init__(self):
        self.game: Game | None = None
