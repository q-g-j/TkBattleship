import pyglet
from utils.files import Files


class Fonts:
    NORMAL_TEXT = "Titillium Web"
    MENU_BUTTON = "Titillium Web"
    MENU_TITLE = "Alphakind"

    @staticmethod
    def init() -> None:
        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file(Files.fixed_path("assets/fonts/Alphakind.ttf"))
        pyglet.font.add_file(Files.fixed_path("assets/fonts/TitilliumWeb.ttf"))
