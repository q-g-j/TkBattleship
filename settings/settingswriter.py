import json
from models.enums import Paths

from models.settings import Settings
from utils.files import Files


class SettingsWriter:
    def __init__(self):
        self.__settings_folder = Files.get_user_config_folder() + "/" + Paths.SETTINGS_FOLDER
        self.__settings_file = self.__settings_folder + "/" + Paths.SETTINGS_FILE

    def write(self, settings: Settings) -> None:
        settings_dict = settings.to_dict()
        settings_json = json.dumps(settings_dict, indent=4)

        try:
            with open(self.__settings_file, "w") as file:
                file.write(settings_json)
        except Exception as e:
            raise Exception(f"Error writing settings file to {self.__settings_file}", e)
