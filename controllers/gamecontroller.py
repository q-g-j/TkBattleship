from ttkthemes import ThemedTk

from events.eventaggregator import EventAggregator
from factories.commandfactory import CommandFactory
from factories.eventhandlerfactory import EventHandlerFactory
from factories.gamefactory import GameFactory
from factories.singleandmultiplayerfactory import SingleAndMultiplayerFactory
from models.enums import OS, Event
from models.game import Game
from models.settings import Settings
from models.singleplayer import SinglePlayer
from models.validator import Validator
from services.injector import DependencyInjector
from settings.settingsreader import SettingsReader
from settings.settingswriter import SettingsWriter
from store.gamestore import GameStore
from utils.files import Files
from utils.messagehelper import MessageHelper
from utils.oshelper import OsHelper
from views.fonts import Fonts
from views.images import Images
from views.mainview import MainView
from views.styles import StyleDefinitions
from views.themes import Themes


class GameController:
    def __init__(self, root: ThemedTk) -> None:
        self.__injector = DependencyInjector()
        self.__root = root

    def start(self) -> None:
        self.__register_services()
        self.__subscribe_events()

        Themes.init(self.__root)
        Images.init()
        Fonts.init()

        self.__root.withdraw()

        self.__root.title("Battleship")
        self.__root.resizable(False, False)

        self.__root.wm_iconphoto(True, Images.ICON)

        if not Files.does_settings_file_exist():
            settings_writer = self.__injector.resolve(SettingsWriter)
            if OsHelper.get_os() == OS.WINDOWS:
                settings_writer.write(Settings(40, "vista"))
            else:
                settings_writer.write(Settings(40, "scidgreen"))

        settings_reader = self.__injector.resolve(SettingsReader)
        settings = settings_reader.read()

        self.__root.config(theme=settings.theme)

        main_view = self.__injector.resolve(MainView)

        main_view.pack()
        main_view.show_menu(1)

        StyleDefinitions.init(self.__root)

        self.__root.update()
        self.__root.deiconify()

    def __register_services(self) -> None:
        game_factory = GameFactory(lambda: self.__injector.resolve(Game))
        single_and_multiplayer_factory = SingleAndMultiplayerFactory(lambda: self.__injector.resolve(SinglePlayer))
        self.__injector.register_instance(game_factory)
        self.__injector.register_instance(single_and_multiplayer_factory)
        self.__injector.register_instance(self.__root)
        self.__injector.add_singleton(EventAggregator)
        self.__injector.add_singleton(GameStore)
        self.__injector.add_singleton(MainView)
        self.__injector.add_transient(CommandFactory)
        self.__injector.add_transient(EventHandlerFactory)
        self.__injector.add_transient(Game)
        self.__injector.add_transient(SinglePlayer)
        self.__injector.add_transient(Validator)
        self.__injector.add_transient(SettingsReader)
        self.__injector.add_transient(SettingsWriter)
        self.__injector.add_transient(MessageHelper)

    def __subscribe_events(self) -> None:
        event_aggregator = self.__injector.resolve(EventAggregator)

        for event in [member.value for member in Event]:
            event_aggregator.subscribe(Event(event), self.__handle_event)

    def __handle_event(self, event: Event, *args) -> None:
        eventhandler_factory = self.__injector.resolve(EventHandlerFactory)

        event_handler = eventhandler_factory.get_event_handler(event)
        event_handler.execute(*args)
