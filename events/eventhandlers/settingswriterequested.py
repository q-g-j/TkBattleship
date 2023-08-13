from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.settings import Settings
from settings.settingswriter import SettingsWriter


class SettingsWriteRequestedEventHandler(EventHandlerBase):
    def __init__(self, settings_writer: SettingsWriter) -> None:
        self.__settings_writer = settings_writer

    def execute(self, settings: Settings) -> None:
        print("works")