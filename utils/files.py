import os, sys
from appdirs import user_config_dir

from models.settings import Settings


class Files:
    # needed for pyinstaller to find the assets:
    @staticmethod
    def fixed_path(filename: str) -> str:
        if hasattr(sys, "_MEIPASS"):
            return getattr(sys, "_MEIPASS") + "/" + filename
        else:
            path = os.path.abspath(".") + "/" + filename
            return path

    @staticmethod
    def get_user_config_folder():
        return user_config_dir()
