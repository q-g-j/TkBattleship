from models.enums import *
from models.ship import Ship
from utils.eventaggregator import EventAggregator


class Game:
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

        self.ships_player = []
        self.ships_opponent = []
        self.playing_field_player = []
        self.playing_field_opponent = []

        self.game_state = GameState.FIRST_RUN
        self.whose_turn = Side.LEFT

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

    def start_multiplayer(self) -> None:
        pass
