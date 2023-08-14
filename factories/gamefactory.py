from models.game import Game
from typing import Callable


class GameFactory:
    def __init__(self, game_resolver: Callable) -> None:
        self.__game_resolver = game_resolver

    def get_game(self) -> Game:
        return self.__game_resolver()
