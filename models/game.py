from random import shuffle, choice

from factories.singleandmultiplayerfactory import SingleAndMultiplayerFactory
from models.enums import *
from models.images import Images
from models.position import Position
from models.ship import Ship
from events.eventaggregator import EventAggregator
from models.singleplayer import SinglePlayer
from services.injector import inject
from utils.messagehelper import MessageHelper


@inject(EventAggregator, SingleAndMultiplayerFactory, MessageHelper)
class Game:
    def __init__(self, event_aggregator: EventAggregator, single_and_multiplayerfactory: SingleAndMultiplayerFactory,
                 message_helper: MessageHelper) -> None:
        self.__event_aggregator = event_aggregator
        self.__single_and_multiplayerfactory = single_and_multiplayerfactory
        self.__message_helper = message_helper

        self.ships_player: list[Ship] = []
        self.ships_opponent: list[Ship] = []
        self.playing_field_player: list[list[str]] = []
        self.playing_field_opponent: list[list[str]] = []

        self.__singleplayer: SinglePlayer | None = None

        self.game_state = GameState.FIRST_RUN
        self.whose_turn = Side.LEFT

        self.__fits_in_direction = Orientation.NONE
        self.num_placed_player_ships = 0

    def create_ships(self, side: Side) -> None:
        for ship_type in ShipTypes:
            for _ in range(ship_type[2]):
                if side & Side.LEFT == Side.LEFT:
                    self.ships_player.append(Ship(ship_type[0], ship_type[1]))
                if side & Side.RIGHT == Side.RIGHT:
                    self.ships_opponent.append(Ship(ship_type[0], ship_type[1]))

    def create_playing_field(self, side: Side) -> None:
        for _ in range(10):
            playing_field_player_inner = []
            playing_field_opponent_inner = []
            for _ in range(10):
                if side & Side.LEFT == Side.LEFT:
                    playing_field_player_inner.append(CellContent.EMPTY)
                if side & Side.RIGHT == Side.RIGHT:
                    playing_field_opponent_inner.append(CellContent.EMPTY)
            if side & Side.LEFT == Side.LEFT:
                self.playing_field_player.append(playing_field_player_inner)
            if side & Side.RIGHT == Side.RIGHT:
                self.playing_field_opponent.append(playing_field_opponent_inner)

    def reset_ships(self, side: Side) -> None:
        if side & Side.LEFT == Side.LEFT:
            self.ships_player.clear()
        if side & Side.RIGHT == Side.RIGHT:
            self.ships_opponent.clear()

        self.create_ships(side)

    def reset_playing_field(self, side: Side) -> None:
        for row in range(10):
            for column in range(10):
                if side & Side.LEFT == Side.LEFT:
                    self.playing_field_player[row][column] = CellContent.EMPTY
                if side & Side.RIGHT == Side.RIGHT:
                    self.playing_field_opponent[row][column] = CellContent.EMPTY

    def player_place_ship(self, validator, pos: Position) -> None:
        current_ship: Ship = self.ships_player[self.num_placed_player_ships]
        positions = current_ship.positions
        playing_field = self.playing_field_player
        ships = self.ships_player

        if playing_field[pos.row][pos.col] != CellContent.EMPTY:
            return

        if len(current_ship.positions) == 0:
            if validator.has_adjacent_cells_occupied(Side.LEFT, pos):
                return
            fits_in_direction = validator.does_ship_fit_at_position(Side.LEFT, pos,
                                                                    current_ship.length)
            if fits_in_direction == Orientation.NONE:
                self.__fits_in_direction = Orientation.NONE
                return
            else:
                self.__fits_in_direction = fits_in_direction
        if len(positions) >= 1:
            if self.__fits_in_direction == Orientation.HORIZONTAL and pos.row != positions[0].row:
                return
            if self.__fits_in_direction == Orientation.VERTICAL and pos.col != positions[0].col:
                return

            possible_positions = validator.get_possible_ship_positions(current_ship)
            if pos not in possible_positions:
                return

        playing_field[pos.row][pos.col] = CellContent.FILLED
        self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, pos, Images.UNDAMAGED_GREEN)

        positions.append(pos)
        if len(positions) == current_ship.length:
            for pos in positions:
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, pos, Images.UNDAMAGED)
            self.num_placed_player_ships += 1

            if self.num_placed_player_ships == len(ships):
                self.__event_aggregator.publish(Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED, False)
                self.__event_aggregator.publish(Event.STATUS_LABEL_TEXT_SENT,
                                                Texts.STATUS_LABEL_PLAYER_TURN)
                self.__message_helper.show(Side.LEFT, [Texts.GAME_STARTED], 0.1)
                self.game_state = GameState.SINGLEPLAYER
            else:
                self.show_message_place_ship(
                    ships[self.num_placed_player_ships], 0.1
                )

    def place_random_ships(self, validator, side: Side) -> None:
        ships = []
        playing_field = []

        if side & Side.LEFT == Side.LEFT:
            ships = self.ships_player
            playing_field = self.playing_field_player
        if side & Side.RIGHT == Side.RIGHT:
            ships = self.ships_opponent
            playing_field = self.playing_field_opponent

        num_placed_ships = 0
        num_tries = 0
        max_tries = 100

        while num_placed_ships != len(ships) and num_tries < max_tries:
            num_placed_ships = 0
            if num_tries != 0:
                self.reset_ships(side)
                self.reset_playing_field(side)

                shuffle(ships)

            ship: Ship
            for ship in ships:
                is_ship_placed = False
                ship.orientation = choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                possible_rows = list(
                    range(10 if ship.orientation == Orientation.HORIZONTAL else 10 - ship.length)
                )
                shuffle(possible_rows)
                possible_columns = list(
                    range(10 if ship.orientation == Orientation.VERTICAL else 10 - ship.length)
                )
                shuffle(possible_columns)
                for row in possible_rows:
                    if is_ship_placed:
                        break
                    for column in possible_columns:
                        if is_ship_placed:
                            break
                        do_place = True
                        positions: list[Position] = []
                        for i in range(ship.length):
                            if ship.orientation == Orientation.HORIZONTAL:
                                positions.append(Position(row, column + i))
                            else:
                                positions.append(Position(row + i, column))
                        for pos in positions:
                            if playing_field[pos.row][pos.col] != CellContent.EMPTY \
                                    or validator.has_adjacent_cells_occupied(side, pos):
                                do_place = False
                                break
                        if do_place:
                            for pos in positions:
                                playing_field[pos.row][pos.col] = CellContent.FILLED
                                ship.positions.append(pos)
                            is_ship_placed = True
                            num_placed_ships += 1
            num_tries += 1

        # print("placed ships: {0}, tries: {1}".format(num_placed_ships, num_tries))

    def show_message_place_ship(self, ship: Ship, delay: float) -> None:
        message = "Place a {0} (length: {1})".format(ship.name, ship.length)
        self.__message_helper.show(Side.LEFT, [message], delay)

    def singleplayer_make_ai_move(self):
        self.__singleplayer.ai_make_move()
        self.whose_turn = Side.LEFT

        if not self.game_state == GameState.GAME_OVER:
            self.__event_aggregator.publish(Event.STATUS_LABEL_TEXT_SENT, Texts.STATUS_LABEL_PLAYER_TURN)

    def start_singleplayer(self, validator):
        self.__singleplayer = self.__single_and_multiplayerfactory.get_singleplayer()

        self.__singleplayer.ai_reset_for_new_game()

        if self.game_state == GameState.FIRST_RUN:
            self.create_ships(Side.BOTH)
            self.create_playing_field(Side.BOTH)
        else:
            self.reset_playing_field(Side.BOTH)
            self.reset_ships(Side.BOTH)
        self.game_state = GameState.PLAYER_PLACING_SHIPS
        self.whose_turn = Side.LEFT

        self.__event_aggregator.publish(
            Event.RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED, True
        )

        self.place_random_ships(validator, Side.RIGHT)

        self.__event_aggregator.publish(Event.STATUS_LABEL_TEXT_SENT, Texts.STATUS_LABEL_SINGLEPLAYER_STARTED)
