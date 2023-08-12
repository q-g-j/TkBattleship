from models.singleplayer import SinglePlayer
from services.injector import DependencyInjector


class SingleAndMultiplayerFactory:
    def __init__(self, injector: DependencyInjector):
        self.__injector = injector

    def get_singleplayer(self) -> SinglePlayer:
        return self.__injector.resolve(SinglePlayer)
