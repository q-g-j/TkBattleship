from tkinter import ttk
from ttkthemes import ThemedTk
from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.settings import Settings
from settings.settingsreader import SettingsReader
from settings.settingswriter import SettingsWriter
import views.styles


class ThemeChangeRequestedEventHandler(EventHandlerBase):
    def __init__(self, root: ThemedTk, settings_reader: SettingsReader, settings_writer: SettingsWriter) -> None:
        self.__root = root
        self.__settings_reader = settings_reader
        self.__settings_writer = settings_writer

    def execute(self, theme: str) -> None:
        style = ttk.Style(self.__root)
        style.theme_use(theme)

        settings = self.__settings_reader.read()

        if settings.theme != theme:
            settings.theme = theme
            self.__settings_writer.write(settings)

        views.styles.StyleDefinitions.init(self.__root, settings)
