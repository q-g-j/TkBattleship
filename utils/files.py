import os
import sys


class Files:
    # needed for pyinstaller to find the assets:
    @staticmethod
    def fixed_path(filename: str) -> str:
        if hasattr(sys, "_MEIPASS"):
            return getattr(sys, "_MEIPASS") + "/" + filename
        else:
            path = os.path.abspath(".") + "/" + filename
            return path
