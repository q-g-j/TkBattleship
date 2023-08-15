import tkinter
from tkinter import ttk
from ttkthemes import ThemedTk

from views.fonts import Fonts


class StyleDefinitions:
    MAIN_VIEW_FRAME = "MainViewFrame.TFrame"

    NOTATION_FRAME = "NotationFrame.TFrame"

    MENU_BUTTON = "MenuButton.TButton"
    RANDOM_SHIPS_BUTTON = "RandomShipsButton.TButton"

    STATUS_LABEL = "StatusLabel.TLabel"

    MENU_FRAME = "MenuFrame.TFrame"
    MENU_ITEM_HEADER_LABEL = "MenuItemHeader.TLabel"
    MENU_ITEM_BUTTON = "MenuItemButton.TButton"
    MENU_ITEM_THEME_BUTTON = "MenuItemThemeButton.TButton"
    MENU_ITEM_QUIT_BUTTON = "MenuItemQuitButton.TButton"

    MESSAGEBOX_FRAME = "MessageBoxFrame.TFrame"
    MESSAGEBOX_LABEL = "Message.TLabel"
    MESSAGEBOX_BUTTON = "Message.TButton"

    CELL_BUTTON = "CellButton.TButton"

    @staticmethod
    def init(root: ThemedTk) -> None:
        style: ttk.Style = ttk.Style(root)

        style.configure(StyleDefinitions.MAIN_VIEW_FRAME)
        style.configure(StyleDefinitions.NOTATION_FRAME, background="transparent")
        style.configure(
            StyleDefinitions.MENU_BUTTON,
            foreground="black",
            font=(Fonts.SELAWIK, 13, "bold"),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.RANDOM_SHIPS_BUTTON, foreground="black", font=(Fonts.SELAWIK, 13), padding=(15, 0, 15, 0)
        )
        style.configure(StyleDefinitions.STATUS_LABEL, padding=(15, 0, 15, 0))
        style.configure(StyleDefinitions.MENU_FRAME, width=100, relief="solid")
        style.configure(StyleDefinitions.MENU_ITEM_HEADER_LABEL, foreground="red")
        style.configure(
            StyleDefinitions.MENU_ITEM_BUTTON,
            foreground="black",
            font=(Fonts.SELAWIK, 12, "bold"),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.MENU_ITEM_THEME_BUTTON,
            foreground="black",
            font=(Fonts.SELAWIK, 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.MENU_ITEM_QUIT_BUTTON,
            foreground="black",
            font=(Fonts.SELAWIK, 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(StyleDefinitions.MESSAGEBOX_FRAME, relief="solid")
        style.configure(StyleDefinitions.MESSAGEBOX_LABEL)
        style.configure(
            StyleDefinitions.MESSAGEBOX_BUTTON,
            foreground="black",
            font=(Fonts.SELAWIK, 11),
        )
        style.configure(StyleDefinitions.CELL_BUTTON, relief=tkinter.FLAT, padding=(0, 0, 0, 0))
