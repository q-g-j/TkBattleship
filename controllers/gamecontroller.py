from tkinter import Tk

from factories.commandfactory import CommandFactory
from factories.eventhandlerfactory import EventHandlerFactory
from models.singleplayer import SinglePlayer
from models.validator import Validator
from events.eventaggregator import EventAggregator
from models.game import Game

from services.injector import DependencyInjector
from utils.messagehelper import MessageHelper
from models.images import Images
from views.mainview import MainView
from models.enums import Event
from models.styles import StyleDefinition


class GameController:
    def __init__(self, injector: DependencyInjector) -> None:
        self.__injector = injector

        self.__root = injector.resolve(Tk)

        StyleDefinition.init(self.__root)
        Images.init()

        self.__register_services()
        self.__subscribe_events()

        MessageHelper.init(self.__injector.resolve(EventAggregator))

    def start(self) -> None:
        main_view = self.__injector.resolve(MainView)

        main_view.pack()
        main_view.show_menu(1)

    def __register_services(self):
        self.__injector.add_singleton(EventAggregator)
        self.__injector.add_singleton(Game)
        self.__injector.add_singleton(CommandFactory)
        self.__injector.add_singleton(EventHandlerFactory)
        self.__injector.add_singleton(MainView)
        self.__injector.add_singleton(Validator)
        self.__injector.add_singleton(SinglePlayer)

    def __subscribe_events(self) -> None:
        event_aggregator = self.__injector.resolve(EventAggregator)

        for event in [member.value for member in Event]:
            event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args):
        eventhandler_factory = self.__injector.resolve(EventHandlerFactory)

        event_handler = eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
