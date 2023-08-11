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
        self.__injector = DependencyInjector()

        self.__root = root

        self.__configure_root_window()
        self.__register_services()
        self.__subscribe_events()

    def start_game(self) -> None:
        main_view = self.__injector.resolve(MainView)

        main_view.pack()
        main_view.show_menu(1)

    def __configure_root_window(self):
        self.__root.title("Battleship")
        self.__root.resizable(False, False)

        StyleDefinition.init(self.__root)
        Images.init()

    def __register_services(self):
        self.__injector.register_instance(self.__root)
        self.__injector.add_singleton(EventAggregator)
        self.__injector.add_singleton(Game)
        self.__injector.add_singleton(CommandFactory)
        self.__injector.add_singleton(EventHandlerFactory)
        self.__injector.add_singleton(MainView)
        self.__injector.add_singleton(Validator)
        self.__injector.add_singleton(SinglePlayer)
        self.__injector.add_singleton(MessageHelper)

    def __subscribe_events(self) -> None:
        event_aggregator = self.__injector.resolve(EventAggregator)

        for event in [member.value for member in Event]:
            event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args):
        eventhandler_factory = self.__injector.resolve(EventHandlerFactory)

        event_handler = eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
