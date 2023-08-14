import pyglet
from utils.files import Files


class Fonts:
    SELAWIK = "Selawk"

    @staticmethod
    def init() -> None:
        pyglet.font.add_file(Files.fixed_path("assets/fonts/Selawik/selawk.ttf"))
