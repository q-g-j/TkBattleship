from tkinter import Tk

from factories.commandfactory import CommandFactory
from factories.eventhandlerfactory import EventHandlerFactory
from models.singleplayer import SinglePlayer
from models.validator import Validator
from events.eventaggregator import EventAggregator
from models.game import Game
from models.settings import Settings
from utils.files import Files
from utils.messagehelper import MessageHelper
from models.images import Images
from views.main import Main
from models.enums import Event
from models.styles import StyleDefinition


class GameController:
    def __init__(self, root: Tk) -> None:
        self.__root = root
        self.__event_aggregator = EventAggregator()

        MessageHelper.init(self.__event_aggregator)
        StyleDefinition.init(root)
        Images.init()
        
        self.__settings = Files.read_settings_from_file()

        self.__game = Game(self.__event_aggregator)
        self.__validator = Validator(self.__game)
        self.__command_factory = CommandFactory(self.__event_aggregator)
        self.__main_view = Main(root, self.__event_aggregator, self.__command_factory, self.__settings)
        self.__singleplayer = SinglePlayer(self.__event_aggregator, self.__game, self.__validator)
        self.__eventhandler_factory = EventHandlerFactory(self.__root, self.__main_view, self.__game,
                                                          self.__validator, self.__singleplayer,
                                                          self.__event_aggregator)

        self.__subscribe_events()

    def start(self) -> None:
        self.__main_view.pack()
        self.__main_view.show_menu(0)

    def __subscribe_events(self) -> None:
        for event in [member.value for member in Event]:
            self.__event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args):
        event_handler = self.__eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
