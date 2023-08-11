from __future__ import annotations
from tkinter import Tk

from events.eventaggregator import EventAggregator
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from events.eventhandlers.quitbuttonclicked import QuitButtonClickedEventHandler
from events.eventhandlers.statuslabeltextsent import StatusLabelEventHandler
from models.enums import Event
from models.game import Game
from models.singleplayer import SinglePlayer
from models.validator import Validator
from services.injector import inject
from views.mainview import MainView

from events.eventhandlers.menubuttonclicked import MenuButtonClickedEventHandler
from events.eventhandlers.randomshipsbuttonvisibilitychanged import RandomShipsButtonVisiblityChangedEventHandler
from events.eventhandlers.singleplayerbuttonclicked import SinglePlayerButtonClickedEventHandler
from events.eventhandlers.cellclicked import CellClickedEventHandler
from events.eventhandlers.messageboxtextsent import MessageBoxTextSentEventHandler
from events.eventhandlers.messageboxclosed import MessageBoxClosedEventHandler
from events.eventhandlers.menuclosed import MenuClosedEventHandler
from events.eventhandlers.cellimageset import CellImageSetEventHandler
from events.eventhandlers.shiphit import ShipHitEventHandler
from events.eventhandlers.randomshipsbuttonclicked import RandomShipsButtonClickedEventHandler
from events.eventhandlers.multiplayerbuttonclicked import MultiplayerButtonClickedEventHandler


@inject("root", "main_view", "game", "validator", "singleplayer", "event_aggregator")
class EventHandlerFactory:
    def __init__(self, root: Tk, main_view: MainView, game: Game, validator: Validator,
                 singleplayer: SinglePlayer, event_aggregator: EventAggregator) -> None:
        self.__root = root
        self.__main_view = main_view
        self.__game = game
        self.__validator = validator
        self.__singleplayer = singleplayer
        self.__event_aggregator = event_aggregator

    def get_event_handler(self, event: Event) -> EventHandlerBase:
        if event == Event.MENU_BUTTON_CLICKED:
            return MenuButtonClickedEventHandler(self.__main_view, self.__game)
        if event == Event.MENU_CLOSED:
            return MenuClosedEventHandler(self.__main_view)
        if event == Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED:
            return RandomShipsButtonVisiblityChangedEventHandler(
                self.__main_view)
        if event == Event.CELL_CLICKED:
            return CellClickedEventHandler(self.__main_view, self.__game, self.__validator,
                                           self.__singleplayer,
                                           self.__event_aggregator)
        if event == Event.MESSAGEBOX_TEXT_SENT:
            return MessageBoxTextSentEventHandler(self.__main_view)
        if event == Event.MESSAGEBOX_CLOSED:
            return MessageBoxClosedEventHandler(self.__main_view)
        if event == Event.CELL_IMAGE_SET:
            return CellImageSetEventHandler(self.__main_view)
        if event == Event.SHIP_HIT:
            return ShipHitEventHandler(self.__main_view,
                                       self.__game,
                                       self.__validator)
        if event == Event.RANDOM_SHIPS_BUTTON_CLICKED:
            return RandomShipsButtonClickedEventHandler(self.__main_view,
                                                        self.__game,
                                                        self.__validator,
                                                        self.__singleplayer)
        if event == Event.MULTIPLAYER_CLICKED:
            return MultiplayerButtonClickedEventHandler()
        if event == Event.SINGLEPLAYER_CLICKED:
            return SinglePlayerButtonClickedEventHandler(self.__main_view, self.__game,
                                                         self.__singleplayer)
        if event == Event.QUIT_BUTTON_CLICKED:
            return QuitButtonClickedEventHandler(self.__root)
        if event == Event.STATUS_LABEL_TEXT_SENT:
            return StatusLabelEventHandler(self.__main_view)
