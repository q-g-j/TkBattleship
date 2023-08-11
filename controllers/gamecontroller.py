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

        MessageHelper.init(self.__injector.resolve(EventAggregator))

    def start(self) -> None:
        main_view = self.__injector.resolve(MainView)

        main_view.pack()
        main_view.show_menu(0)
        
    def __register_services(self):
        self.__injector.register("root", self.__root)

        event_aggregator = self.__injector.resolve(EventAggregator)
        self.__injector.register("event_aggregator", event_aggregator)

        game = self.__injector.resolve(Game)
        self.__injector.register("game", game)

        validator = self.__injector.resolve(Validator)
        self.__injector.register("validator", validator)

        command_factory = self.__injector.resolve(CommandFactory)
        self.__injector.register("command_factory", command_factory)

        main_view = self.__injector.resolve(MainView)
        self.__injector.register("main_view", main_view)

        singleplayer = self.__injector.resolve(SinglePlayer)
        self.__injector.register("singleplayer", singleplayer)

        eventhandler_factory = self.__injector.resolve(EventHandlerFactory)
        self.__injector.register("eventhandler_factory", eventhandler_factory)

    def __subscribe_events(self) -> None:
        event_aggregator = self.__injector.resolve(EventAggregator)

        for event in [member.value for member in Event]:
            event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args):
        eventhandler_factory = self.__injector.resolve(EventHandlerFactory)

        event_handler = eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
