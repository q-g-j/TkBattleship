from PIL import Image, ImageTk
import tkinter as tk

from utils.files import Files


class ImageFiles:
    EMPTY = Files.fixed_path("assets/images/empty.png")
    SHIP = Files.fixed_path("assets/images/ship.png")
    SHIP_BLUE = Files.fixed_path("assets/images/ship_blue.png")
    SHIP_RED = Files.fixed_path("assets/images/ship_red.png")
    SHIP_GREEN = Files.fixed_path("assets/images/ship_green.png")
    HIT = Files.fixed_path("assets/images/hit.png")
    DESTROYED = Files.fixed_path("assets/images/destroyed.png")
    SPLASH = Files.fixed_path("assets/images/splash.png")

    ICON = Files.fixed_path("assets/icons/icon.png")
    ICON_ICO = Files.fixed_path("assets/icons/icon.ico")


class Images(object):
    EMPTY: tk.Image = None
    SHIP: tk.Image = None
    SHIP_BLUE: tk.Image = None
    SHIP_RED: tk.Image = None
    SHIP_GREEN: tk.Image = None
    HIT: tk.Image = None
    DESTROYED: tk.Image = None
    SPLASH: tk.Image = None

    ICON: tk.Image = None

    @staticmethod
    def init() -> None:
        image_empty: Image.Image = Image.open(ImageFiles.EMPTY)
        image_ship: Image.Image = Image.open(ImageFiles.SHIP).resize((32, 32))
        image_ship_blue: Image.Image = Image.open(ImageFiles.SHIP_BLUE).resize((32, 32))
        image_ship_red: Image.Image = Image.open(ImageFiles.SHIP_RED).resize((32, 32))
        image_ship_green: Image.Image = Image.open(ImageFiles.SHIP_GREEN).resize((32, 32))
        image_hit: Image.Image = Image.open(ImageFiles.HIT).resize((25, 25))
        image_destroyed: Image.Image = Image.open(ImageFiles.DESTROYED).resize((25, 25))
        image_splash: Image.Image = Image.open(ImageFiles.SPLASH).resize((25, 25))

        image_icon: Image.Image = Image.open(ImageFiles.ICON)

        Images.EMPTY = ImageTk.PhotoImage(image_empty)
        Images.SHIP = ImageTk.PhotoImage(image_ship)
        Images.SHIP_BLUE = ImageTk.PhotoImage(image_ship_blue)
        Images.SHIP_RED = ImageTk.PhotoImage(image_ship_red)
        Images.SHIP_GREEN = ImageTk.PhotoImage(image_ship_green)
        Images.HIT = ImageTk.PhotoImage(image_hit)
        Images.DESTROYED = ImageTk.PhotoImage(image_destroyed)
        Images.SPLASH = ImageTk.PhotoImage(image_splash)

        Images.ICON_PNG = ImageTk.PhotoImage(image_icon)
