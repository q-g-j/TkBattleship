from __future__ import annotations
from tkinter import Tk

from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from events.eventhandlers.quitbuttonclicked import QuitButtonClickedEventHandler
from events.eventhandlers.statuslabeltextsent import StatusLabelEventHandler
from factories.gamefactory import GameFactory
from models.enums import Event
from models.validator import Validator
from services.injector import inject
from store.gamestore import GameStore
from utils.messagehelper import MessageHelper
from views.mainview import MainView

from events.eventhandlers.menubuttonclicked import MenuButtonClickedEventHandler
from events.eventhandlers.randomshipsbuttonvisibilitychanged import (
    RandomShipsButtonVisiblityChangedEventHandler,
)
from events.eventhandlers.singleplayerbuttonclicked import (
    SinglePlayerButtonClickedEventHandler,
)
from events.eventhandlers.cellclicked import CellClickedEventHandler
from events.eventhandlers.messageboxtextsent import MessageBoxTextSentEventHandler
from events.eventhandlers.messageboxclosed import MessageBoxClosedEventHandler
from events.eventhandlers.menuclosed import MenuClosedEventHandler
from events.eventhandlers.cellimageset import CellImageSetEventHandler
from events.eventhandlers.shiphit import ShipHitEventHandler
from events.eventhandlers.randomshipsbuttonclicked import (
    RandomShipsButtonClickedEventHandler,
)
from events.eventhandlers.multiplayerbuttonclicked import (
    MultiplayerButtonClickedEventHandler,
)


@inject(Tk, MainView, GameFactory, GameStore, Validator, EventAggregator, MessageHelper)
class EventHandlerFactory:
    def __init__(
            self,
            root: Tk,
            main_view: MainView,
            game_factory: GameFactory,
            game_store: GameStore,
            validator: Validator,
            event_aggregator: EventAggregator,
            message_helper: MessageHelper,
    ) -> None:
        self.__root = root
        self.__main_view = main_view
        self.__game_factory = game_factory
        self.__game_store = game_store
        self.__validator = validator
        self.__event_aggregator = event_aggregator
        self.__message_helper = message_helper

    def get_event_handler(self, event: Event) -> EventHandlerBase:
        if event == Event.MENU_BUTTON_CLICKED:
            return MenuButtonClickedEventHandler(self.__main_view, self.__game_store)

        if event == Event.MENU_CLOSED:
            return MenuClosedEventHandler(self.__main_view)

        if event == Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED:
            return RandomShipsButtonVisiblityChangedEventHandler(self.__main_view)

        if event == Event.CELL_CLICKED:
            return CellClickedEventHandler(
                self.__main_view,
                self.__game_store,
                self.__validator,
                self.__event_aggregator,
            )

        if event == Event.MESSAGEBOX_TEXT_SENT:
            return MessageBoxTextSentEventHandler(self.__main_view)

        if event == Event.MESSAGEBOX_CLOSED:
            return MessageBoxClosedEventHandler(self.__main_view)

        if event == Event.CELL_IMAGE_SET:
            return CellImageSetEventHandler(self.__main_view)

        if event == Event.SHIP_HIT:
            return ShipHitEventHandler(
                self.__main_view, self.__game_store, self.__validator, self.__message_helper
            )

        if event == Event.RANDOM_SHIPS_BUTTON_CLICKED:
            return RandomShipsButtonClickedEventHandler(
                self.__main_view, self.__game_store, self.__validator
            )

        if event == Event.SINGLEPLAYER_CLICKED:
            return SinglePlayerButtonClickedEventHandler(
                self.__main_view, self.__game_factory, self.__game_store, self.__validator
            )

        if event == Event.MULTIPLAYER_CLICKED:
            return MultiplayerButtonClickedEventHandler()

        if event == Event.QUIT_BUTTON_CLICKED:
            return QuitButtonClickedEventHandler(self.__root)

        if event == Event.STATUS_LABEL_TEXT_SENT:
            return StatusLabelEventHandler(self.__main_view)
