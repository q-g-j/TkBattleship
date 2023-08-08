from tkinter import Tk, ttk


class StyleDefinition:
    MENU_BUTTON = "MenuButton.TButton"

    MENU_ITEM_HEADER_LABEL = "MenuItemHeader.TLabel"
    MENU_ITEM_BUTTON = "MenuItemButton.TButton"

    MESSAGEBOX_LABEL = "Message.TLabel"
    MESSAGEBOX_BUTTON = "Message.TButton"

    @staticmethod
    def init(root: Tk) -> None:
        style = ttk.Style(root)

        style.configure(
            StyleDefinition.MENU_BUTTON,
            foreground="black",
            background="darkgray",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )

        style.configure(
            StyleDefinition.MENU_ITEM_HEADER_LABEL,
            foreground="red",
            background="darkgray",
            font=("Helvetica", 16),
        )
        style.configure(
            StyleDefinition.MENU_ITEM_BUTTON,
            foreground="blue",
            background="darkgray",
            font=("Helvetica", 12),
            padding=(15, 0, 15, 0),
        )

        style.configure(
            StyleDefinition.MESSAGEBOX_LABEL,
            foreground="red",
            background="darkgray",
            font=("Helvetica", 16),
        )
        style.configure(
            StyleDefinition.MESSAGEBOX_BUTTON,
            foreground="black",
            background="darkgray",
            font=("Helvetica", 12),
        )
