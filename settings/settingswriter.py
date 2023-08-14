import json

from models.settings import Settings
from utils.files import Files


class SettingsWriter:
    def __init__(self) -> None:
        self.__settings_file = Files.get_settings_file_full_path()

    def write(self, settings: Settings) -> None:
        Files.create_settings_folder()

        settings_dict = settings.to_dict()
        settings_json = json.dumps(settings_dict, indent=4)

        try:
            with open(self.__settings_file, "w") as file:
                file.write(settings_json)
        except Exception as e:
            raise Exception(f"Error writing settings file to {self.__settings_file}", e)
