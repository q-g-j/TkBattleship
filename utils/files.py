import os, sys
from appdirs import user_config_dir
from models.enums import Paths


class Files:
    # needed for pyinstaller to find the assets:
    @staticmethod
    def fixed_path(file_or_path: str) -> str:
        if hasattr(sys, "_MEIPASS"):
            return getattr(sys, "_MEIPASS") + "/" + file_or_path
        else:
            path = os.path.abspath(".") + "/" + file_or_path
            return path

    @staticmethod
    def get_user_config_folder() -> str:
        return user_config_dir()

    @staticmethod
    def get_settings_file_full_path() -> str:
        return "{0}/{1}/{2}".format(Files.get_user_config_folder(), Paths.SETTINGS_FOLDER, Paths.SETTINGS_FILE)

    @staticmethod
    def does_settings_file_exist() -> bool:
        return os.path.exists(Files.get_settings_file_full_path())

    @staticmethod
    def create_settings_folder() -> None:
        settings_folder = Files.get_user_config_folder() + "/" + Paths.SETTINGS_FOLDER
        try:
            if not os.path.exists(settings_folder):
                os.makedirs(settings_folder)
        except Exception as e:
            raise Exception(f"Error creating settings folder in {settings_folder}", e)
