from tkinter import Tk
from controllers.gamecontroller import GameController
from services.injector import DependencyInjector


def main() -> None:
    injector = DependencyInjector()
    injector.add_singleton(Tk)

    root = injector.resolve(Tk)

    root.title("Battleship")
    root.resizable(False, False)

    controller = GameController(injector)
    controller.start()

    root.mainloop()


if __name__ == "__main__":
    main()
