from tkinter import Tk
from controllers.gamecontroller import GameController
from services.injector import DependencyInjector


def main() -> None:
    root = Tk()

    root.title("Battleship")
    root.resizable(False, False)

    controller = GameController(root)
    controller.start()

    root.mainloop()


if __name__ == "__main__":
    main()
