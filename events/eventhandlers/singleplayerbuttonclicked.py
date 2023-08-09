from events.eventhandlers.eventhandlerbase import EventHandlerBase
from models.debug import Debug
from models.enums import Side


class SinglePlayerButtonClickedEventHandler(EventHandlerBase):
    def __init__(self, main_view, game, singleplayer):
        self.__main_view = main_view
        self.__game = game
        self.__singleplayer = singleplayer

    def execute(self):
        self.__main_view.close_menu()
        self.__main_view.clear_cells(Side.BOTH)
        self.__singleplayer.start()

        Debug.print_playing_field(self.__game.playing_field_opponent)

        self.__singleplayer.show_message_place_ship(self.__game.ships_player[0], 0)