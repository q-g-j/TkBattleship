from tkinter import Tk

from controllers.gamecontroller import GameController


def main() -> None:
    root = Tk()

    controller = GameController(root)
    controller.start_game()

    root.mainloop()


if __name__ == "__main__":
    main()
