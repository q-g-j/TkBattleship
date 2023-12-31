from models.enums import Texts
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from store.gamestore import GameStore
from utils.sleep import threaded_sleep
from views.mainview import MainView


class AINextMoveRequestedEventHandler(EventHandlerBase):
    def __init__(self, game_store: GameStore, main_view: MainView) -> None:
        self.__game_store = game_store
        self.__main_view = main_view

    def execute(self) -> None:
        self.__main_view.set_status_label_text(Texts.STATUS_LABEL_AI_TURN)
        threaded_sleep(lambda: self.__game_store.game.singleplayer_make_ai_move(), 0.4)
