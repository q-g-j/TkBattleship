from models.game import Game
from services.injector import DependencyInjector


class GameFactory:
    def __init__(self, injector: DependencyInjector):
        self.__injector = injector

    def get_game(self) -> Game:
        return self.__injector.resolve(Game)
