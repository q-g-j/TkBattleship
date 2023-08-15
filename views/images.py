from PIL import Image, ImageTk
import tkinter as tk

from utils.files import Files


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
        empty = Files.fixed_path("assets/images/empty.png")
        ship_black = Files.fixed_path("assets/images/ship.png")
        ship_blue = Files.fixed_path("assets/images/ship_blue.png")
        ship_red = Files.fixed_path("assets/images/ship_red.png")
        ship_green = Files.fixed_path("assets/images/ship_green.png")
        hit = Files.fixed_path("assets/images/hit.png")
        destroyed = Files.fixed_path("assets/images/destroyed.png")
        splash = Files.fixed_path("assets/images/splash.png")

        icon = Files.fixed_path("assets/icons/battleship.png")

        image_empty: Image.Image = Image.open(empty)
        image_ship: Image.Image = Image.open(ship_black).resize((32, 32))
        image_ship_blue: Image.Image = Image.open(ship_blue).resize((32, 32))
        image_ship_red: Image.Image = Image.open(ship_red).resize((32, 32))
        image_ship_green: Image.Image = Image.open(ship_green).resize((32, 32))
        image_hit: Image.Image = Image.open(hit).resize((25, 25))
        image_destroyed: Image.Image = Image.open(destroyed).resize((25, 25))
        image_splash: Image.Image = Image.open(splash).resize((25, 25))

        image_icon: Image.Image = Image.open(icon).resize((64, 64))

        Images.EMPTY = ImageTk.PhotoImage(image_empty)
        Images.SHIP = ImageTk.PhotoImage(image_ship)
        Images.SHIP_BLUE = ImageTk.PhotoImage(image_ship_blue)
        Images.SHIP_RED = ImageTk.PhotoImage(image_ship_red)
        Images.SHIP_GREEN = ImageTk.PhotoImage(image_ship_green)
        Images.HIT = ImageTk.PhotoImage(image_hit)
        Images.DESTROYED = ImageTk.PhotoImage(image_destroyed)
        Images.SPLASH = ImageTk.PhotoImage(image_splash)

        Images.ICON = ImageTk.PhotoImage(image_icon)
