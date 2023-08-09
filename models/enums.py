from enum import Enum, IntFlag


class Command(Enum):
    # MainView:
    MENU_BUTTON_CLICKED = 1
    CELL_CLICKED = 2
    RANDOM_SHIPS_BUTTON_CLICKED = 3

    # Menu:
    START_SINGLEPLAYER = 4
    START_MULTIPLAYER = 5
    QUIT_GAME = 6



class Event(Enum):
    MENU_BUTTON_CLICKED = 1
    QUIT_BUTTON_CLICKED = 2
    MENU_CLOSED = 3
    SINGLEPLAYER_CLICKED = 4
    MULTIPLAYER_CLICKED = 5
    CELL_CLICKED = 6
    MESSAGEBOX_TEXT_SENT = 7
    MESSAGEBOX_CLOSED = 8
    CELL_IMAGE_SET = 9
    CHECK_SHIP_DESTROYED_REQUESTED = 10
    RANDOM_SHIPS_BUTTON_CLICKED = 11
    RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED = 12


class CellContent:
    EMPTY = " "
    FILLED = "X"
    DESTROYED = "D"


class GameState(Enum):
    FIRST_RUN = 0
    SINGLE_PLAYER = 1
    MULTIPLAYER = 2
    GAME_OVER = 3
    PLAYER_PLACING_SHIPS = 4


NotationColumns = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
}

ShipTypes = [
    # ("name", length, number_to_place)
    ("Destroyer", 2, 2),
    ("Cruiser", 3, 1),
    ("Submarine", 3, 2),
    ("Battleship", 4, 1),
    ("Carrier", 5, 1),
]


class Side(IntFlag):
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    BOTH = LEFT | RIGHT


class Direction(IntFlag):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = HORIZONTAL | VERTICAL
