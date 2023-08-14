import json

from models.settings import Settings
from utils.files import Files


class SettingsReader:
    def __init__(self) -> None:
        self.__settings_file = Files.get_settings_file_full_path()

    def read(self) -> Settings:
        with open(self.__settings_file, "r") as file:
            settings_json = json.load(file)

            return Settings(**settings_json)
