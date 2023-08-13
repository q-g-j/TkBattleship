import tkinter
from tkinter import Tk, ttk


class StyleDefinitions:
    MAIN_VIEW_FRAME = "MainViewFrame.TFrame"
    
    MENU_BUTTON = "MenuButton.TButton"
    RANDOM_SHIPS_BUTTON = "RandomShipsButton.TButton"

    STATUS_LABEL = "StatusLabel.TLabel"

    MENU_FRAME = "MenuFrame.TFrame"
    MENU_ITEM_HEADER_LABEL = "MenuItemHeader.TLabel"
    MENU_ITEM_BUTTON = "MenuItemButton.TButton"

    MESSAGEBOX_FRAME = "MessageBoxFrame.TFrame"
    MESSAGEBOX_LABEL = "Message.TLabel"
    MESSAGEBOX_BUTTON = "Message.TButton"

    CELL_BUTTON = "CellButton.TButton"

    @staticmethod
    def init(root: Tk) -> None:
        style: ttk.Style = ttk.Style(root)

        style.configure(
            StyleDefinitions.MAIN_VIEW_FRAME,
        )
        style.configure(
            StyleDefinitions.MENU_BUTTON,
            foreground="black",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.RANDOM_SHIPS_BUTTON,
            foreground="black",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.STATUS_LABEL,
            foreground="blue",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.MENU_FRAME,
            relief="solid"
        )
        style.configure(
            StyleDefinitions.MENU_ITEM_HEADER_LABEL,
            foreground="red",
            font=("Helvetica", 16),
        )
        style.configure(
            StyleDefinitions.MENU_ITEM_BUTTON,
            foreground="blue",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )
        style.configure(
            StyleDefinitions.MESSAGEBOX_FRAME,
            relief="solid"
        )
        style.configure(
            StyleDefinitions.MESSAGEBOX_LABEL,
            foreground="red",
            font=("Helvetica", 16),
        )
        style.configure(
            StyleDefinitions.MESSAGEBOX_BUTTON,
            foreground="black",
            font=("Helvetica", 12),
        )
        style.configure(
            StyleDefinitions.CELL_BUTTON,
            relief=tkinter.FLAT
        )
