from __future__ import annotations

from ttkthemes import ThemedTk

from events.eventaggregator import EventAggregator
from events.eventhandlers.ainextmoverequestedeventhandler import AINextMoveRequestedEventHandler
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from events.eventhandlers.quitbuttonclicked import QuitButtonClickedEventHandler
from events.eventhandlers.statuslabeltextsent import StatusLabelTextSentEventHandler
from events.eventhandlers.themechangerequested import ThemeChangeRequestedEventHandler
from events.eventhandlers.menubuttonclicked import MenuButtonClickedEventHandler
from events.eventhandlers.randomshipsbuttonvisibilitychanged import (
    RandomShipsButtonVisiblityChangedEventHandler,
)
from events.eventhandlers.singleplayerbuttonclicked import (
    SinglePlayerButtonClickedEventHandler,
)
from events.eventhandlers.cellclicked import CellClickedEventHandler
from events.eventhandlers.messageboxtextsent import MessageBoxTextSentEventHandler
from events.eventhandlers.messageboxclosed import MessageBoxCloseRequestedEventHandler
from events.eventhandlers.menuclosed import MenuClosedEventHandler
from events.eventhandlers.cellimageset import CellImageSetEventHandler
from events.eventhandlers.shiphit import ShipHitEventHandler
from events.eventhandlers.randomshipsbuttonclicked import (
    RandomShipsButtonClickedEventHandler,
)
from events.eventhandlers.multiplayerbuttonclicked import (
    MultiplayerButtonClickedEventHandler,
)
from factories.gamefactory import GameFactory
from models.enums import Event
from models.validator import Validator
from services.injector import inject
from store.gamestore import GameStore
from utils.messagehelper import MessageHelper
from views.mainview import MainView
from settings.settingsreader import SettingsReader
from settings.settingswriter import SettingsWriter


@inject(
    ThemedTk,
    MainView,
    GameFactory,
    GameStore,
    Validator,
    EventAggregator,
    MessageHelper,
    SettingsReader,
    SettingsWriter,
)
class EventHandlerFactory:
    def __init__(
        self,
        root: ThemedTk,
        main_view: MainView,
        game_factory: GameFactory,
        game_store: GameStore,
        validator: Validator,
        event_aggregator: EventAggregator,
        message_helper: MessageHelper,
        settings_reader: SettingsReader,
        settings_writer: SettingsWriter,
    ) -> None:
        self.__root = root
        self.__main_view = main_view
        self.__game_factory = game_factory
        self.__game_store = game_store
        self.__validator = validator
        self.__event_aggregator = event_aggregator
        self.__message_helper = message_helper
        self.__settings_reader = settings_reader
        self.__settings_writer = settings_writer

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

        if event == Event.MESSAGEBOX_CLOSE_REQUESTED:
            return MessageBoxCloseRequestedEventHandler(self.__main_view)

        if event == Event.CELL_IMAGE_SET:
            return CellImageSetEventHandler(self.__main_view)

        if event == Event.SHIP_HIT:
            return ShipHitEventHandler(
                self.__main_view, self.__game_store, self.__validator, self.__message_helper, self.__event_aggregator
            )

        if event == Event.RANDOM_SHIPS_BUTTON_CLICKED:
            return RandomShipsButtonClickedEventHandler(self.__main_view, self.__game_store, self.__validator)

        if event == Event.SINGLEPLAYER_CLICKED:
            return SinglePlayerButtonClickedEventHandler(
                self.__main_view, self.__game_factory, self.__game_store, self.__validator
            )

        if event == Event.MULTIPLAYER_CLICKED:
            return MultiplayerButtonClickedEventHandler()

        if event == Event.QUIT_BUTTON_CLICKED:
            return QuitButtonClickedEventHandler(self.__root)

        if event == Event.STATUS_LABEL_TEXT_SENT:
            return StatusLabelTextSentEventHandler(self.__main_view)

        if event == Event.AI_NEXT_MOVE_REQUESTED:
            return AINextMoveRequestedEventHandler(self.__game_store, self.__main_view)

        if event == Event.THEME_CHANGE_REQUESTED:
            return ThemeChangeRequestedEventHandler(self.__root, self.__settings_reader, self.__settings_writer)
