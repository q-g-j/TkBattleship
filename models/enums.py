from enum import Enum, IntFlag


class OS:
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "Darwin"


class Paths:
    SETTINGS_FOLDER = "TkBattleship"
    SETTINGS_FILE = "settings.json"


class Command(Enum):
    # MainView:
    OPEN_MENU = 1
    CELL_CLICK = 2
    PLACE_RANDOM_SHIPS = 3

    # Menu:
    START_SINGLE_PLAYER = 4
    START_MULTIPLAYER = 5
    CHANGE_THEME = 6
    QUIT_GAME = 7


class Event(Enum):
    MENU_BUTTON_CLICKED = 1
    QUIT_BUTTON_CLICKED = 2
    MENU_CLOSED = 3
    SINGLEPLAYER_CLICKED = 4
    MULTIPLAYER_CLICKED = 5
    CELL_CLICKED = 6
    MESSAGEBOX_TEXT_SENT = 7
    MESSAGEBOX_CLOSE_REQUESTED = 8
    CELL_IMAGE_SET = 9
    SHIP_HIT = 10
    RANDOM_SHIPS_BUTTON_CLICKED = 11
    RANDOM_SHIPS_BUTTON_VISIBILITY_CHANGED = 12
    STATUS_LABEL_TEXT_SENT = 13
    AI_NEXT_MOVE_REQUESTED = 14
    THEME_CHANGE_REQUESTED = 15


class CellContent:
    EMPTY = " "
    FILLED = "X"
    DESTROYED = "D"


class GameState(Enum):
    FIRST_RUN = 0
    SINGLEPLAYER = 1
    MULTIPLAYER = 2
    GAME_OVER = 3
    PLAYER_PLACING_SHIPS = 4


class Difficulty(Enum):
    EASY = 1
    NORMAL = 2


class Texts:
    STATUS_LABEL_SINGLEPLAYER_STARTED = "Singleplayer game started!"
    STATUS_LABEL_PLAYER_TURN = "It's your turn."
    STATUS_LABEL_AI_TURN = "It's the computer's turn."
    STATUS_LABEL_OPPONENT_TURN = "It's your opponents's turn."

    GAME_STARTED = "Game started!"

    PLAYER_WON = "You have won!"
    OPPONENT_WON = "Your opponent has won!"
    AI_WON = "The computer has won!"


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
    ("Destroyer", 2, 3),
    ("Submarine", 3, 2),
    ("Cruiser", 3, 1),
    ("Battleship", 4, 1),
    ("Carrier", 5, 1),
]

# ShipTypes = [
#     # ("name", length, number_to_place)
#     ("Carrier", 5, 5),
# ]


class Side(IntFlag):
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    BOTH = LEFT | RIGHT


class Orientation(IntFlag):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = HORIZONTAL | VERTICAL
