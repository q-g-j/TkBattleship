import platform

from models.enums import OS


class OsHelper:
    @staticmethod
    def get_os() -> OS:
        operating_system = platform.system()
        print(operating_system)
        if operating_system in [eval(f"OS.{member}") for member in dir(OS)]:
            return operating_system
        else:
            raise Exception("Unknown operating system")
