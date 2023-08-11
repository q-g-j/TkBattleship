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
    def __init__(self, root: Tk) -> None:
        self.__root = root
        self.__injector = DependencyInjector()

        StyleDefinition.init(self.__root)
        Images.init()
        
        self.__register_services()        
        self.__subscribe_events()

        MessageHelper.init(self.__event_aggregator)

    def start(self) -> None:
        self.__main_view.pack()
        self.__main_view.show_menu(0)
        
    def __register_services(self):
        self.__injector.register("root", self.__root)

        self.__event_aggregator = self.__injector.resolve(EventAggregator)
        self.__injector.register("event_aggregator", self.__event_aggregator)

        self.__game = self.__injector.resolve(Game)
        self.__injector.register("game", self.__game)

        self.__validator = self.__injector.resolve(Validator)
        self.__injector.register("validator", self.__validator)

        self.__command_factory = self.__injector.resolve(CommandFactory)
        self.__injector.register("command_factory", self.__command_factory)

        self.__main_view = self.__injector.resolve(MainView)
        self.__injector.register("main_view", self.__main_view)

        self.__singleplayer = self.__injector.resolve(SinglePlayer)
        self.__injector.register("singleplayer", self.__singleplayer)

        self.__eventhandler_factory = self.__injector.resolve(EventHandlerFactory)
        self.__injector.register("eventhandler_factory", self.__eventhandler_factory)

    def __subscribe_events(self) -> None:
        for event in [member.value for member in Event]:
            self.__event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args):
        event_handler = self.__eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
