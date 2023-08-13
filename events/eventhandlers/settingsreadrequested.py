from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.settings import Settings
from settings.settingsreader import SettingsReader


class SettingsReadRequestedEventHandler(EventHandlerBase):
    def __init__(self, settings_reader: SettingsReader) -> None:
        self.__settings_reader = settings_reader

    def execute(self) -> Settings:
        return self.__settings_reader.read()
