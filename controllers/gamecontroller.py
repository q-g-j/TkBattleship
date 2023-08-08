from tkinter import Tk

from PIL import ImageTk

from models.ship import Ship
from models.singleplayer import SinglePlayer
from models.validator import Validator
from utils.debug import Debug
from utils.eventaggregator import EventAggregator
from models.game import Game
from utils.messagehelper import MessageHelper
from models.images import Images
from views.mainview import MainView
from models.enums import Event, GameState, Side
from models.styles import StyleDefinition


class GameController:
    def __init__(self, root: Tk) -> None:
        self.__root = root
        self.__event_aggregator = EventAggregator()

        MessageHelper.init(self.__event_aggregator)
        StyleDefinition.init(root)
        Images.init()

        self.__game = Game(self.__event_aggregator)
        self.__validator = Validator(self.__game.playing_field_player, self.__game.playing_field_opponent,
                                     self.__game.ships_player, self.__game.ships_opponent)
        self.__main_view = MainView(root, self.__event_aggregator)

        self.__singleplayer = None
        self.__is_menu_open = False
        self.__is_messagebox_open = False

        self.__subscribe_events()

    def start(self) -> None:
        self.__main_view.pack()
        self.__is_menu_open = True
        self.__main_view.show_menu(0)

    def __subscribe_events(self) -> None:
        self.__event_aggregator.subscribe(
            Event.MENU_BUTTON_CLICKED, self.__handle_menu_button_clicked
        )
        self.__event_aggregator.subscribe(
            Event.SINGLEPLAYER_CLICKED, self.__handle_singleplayer_clicked
        )
        self.__event_aggregator.subscribe(
            Event.MULTIPLAYER_CLICKED, self.__handle_multiplayer_clicked
        )
        self.__event_aggregator.subscribe(
            Event.QUIT_BUTTON_CLICKED, self.__handle_quit_clicked
        )
        self.__event_aggregator.subscribe(Event.MENU_CLOSED, self.__handle_menu_closed)
        self.__event_aggregator.subscribe(
            Event.CELL_CLICKED, self.__handle_cell_clicked
        )
        self.__event_aggregator.subscribe(
            Event.MESSAGEBOX_TEXT_SENT, self.__handle_message_sent
        )
        self.__event_aggregator.subscribe(
            Event.MESSAGEBOX_CLOSED, self.__handle_messagebox_closed
        )
        self.__event_aggregator.subscribe(Event.CELL_IMAGE_SET, self.__handle_placed_mark)
        self.__event_aggregator.subscribe(Event.CHECK_IF_SHIP_DESTROYED, self.__handle_check_if_ship_destroyed)

    def __handle_menu_button_clicked(self) -> None:
        if self.__is_messagebox_open:
            self.__main_view.close_messagebox()
        if not self.__is_menu_open:
            self.__main_view.show_menu()
            self.__is_menu_open = True
        else:
            if self.__game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()

    def __handle_singleplayer_clicked(self) -> None:
        self.__main_view.clear_cells(Side.BOTH)
        self.__singleplayer = SinglePlayer(self.__event_aggregator, self.__game, self.__validator)
        self.__singleplayer.start()

        Debug.print_playing_field(self.__game.playing_field_opponent)
        print()

        if Debug.PLAYER_PLACE_RANDOM_SHIPS:
            self.__singleplayer.place_random_ships(Side.LEFT)

            for ship in self.__game.ships_player:
                for pos in ship.positions:
                    self.__main_view.place_mark(Side.LEFT, pos[0], pos[1], Images.UNDAMAGED)
            self.__game.game_state = GameState.SINGLE_PLAYER
        else:
            self.__singleplayer.show_message_place_ship(self.__game.ships_player[0], 0)

    def __handle_multiplayer_clicked(self) -> None:
        self.__main_view.clear_cells(Side.LEFT)
        self.__main_view.clear_cells(Side.RIGHT)
        self.__game.start_multiplayer()

    def __handle_quit_clicked(self) -> None:
        self.__root.destroy()

    def __handle_menu_closed(self) -> None:
        self.__is_menu_open = False

    def __handle_messagebox_closed(self) -> None:
        self.__is_messagebox_open = False

    def __handle_cell_clicked(self, field_side: Side, row: int, column: int) -> None:
        # close the menu if open and RETURN:
        if self.__is_menu_open:
            if self.__game.game_state != GameState.FIRST_RUN:
                self.__main_view.close_menu()
                return

        # close the messagebox if open and RETURN:
        if self.__is_messagebox_open:
            self.__main_view.close_messagebox()
            return

        # don't allow cell clicks on first run and game over:
        if self.__game.game_state in (
                GameState.FIRST_RUN,
                GameState.GAME_OVER,
        ):
            return

        # if player is currently placing ships:
        if self.__game.game_state == GameState.PLAYER_PLACING_SHIPS:

            # don't allow clicks on the right side:
            if field_side == Side.RIGHT:
                return

            # go to function Singleplayer.player_place_ship(), then RETURN:
            if field_side == Side.LEFT:
                self.__singleplayer.player_place_ship(row, column)
                return

        # finally:
        # if cell is filled, mark it as hit and check if ship is destroyed:
        if not self.__validator.is_cell_empty(field_side, row, column):
            self.__main_view.place_mark(field_side, row, column, Images.HIT)
            self.__handle_check_if_ship_destroyed(Side.RIGHT, row, column)

        # singleplayer mode: let the AI make it's move:
        if self.__game.whose_turn == Side.LEFT and self.__game.game_state == GameState.SINGLE_PLAYER:
            self.__singleplayer.ai_make_move()

    def __handle_message_sent(self, field_side: Side, messages: list) -> None:
        self.__is_messagebox_open = True
        self.__main_view.show_messagebox(field_side, messages)

    def __handle_placed_mark(
            self, field_side: Side, row: int, column: int, image: ImageTk.PhotoImage
    ) -> None:
        self.__main_view.place_mark(field_side, row, column, image)

    def __handle_check_if_ship_destroyed(self, side: Side, row: int, column: int):
        ship: Ship = self.__validator.get_destroyed_ship(
            side, row, column)
        if ship is not None:
            self.__main_view.mark_cells_destroyed(side, ship.positions)
            messages = ["{0} sunk!".format(ship.name)]
            if self.__validator.are_all_ships_destroyed(side):
                self.__game.game_state = GameState.GAME_OVER
                messages.append("Game over!")

            MessageHelper.show(side, messages, 0.3)
