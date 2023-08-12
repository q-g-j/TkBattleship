from models.singleplayer import SinglePlayer
from typing import Callable


class SingleAndMultiplayerFactory:
    def __init__(self, singleplayer_resolver: Callable):
        self.__singleplayer_resolver = singleplayer_resolver

    def get_singleplayer(self) -> SinglePlayer:
        return self.__singleplayer_resolver()
