from tkinter import Tk
from controllers.gamecontroller import GameController
from utils.files import Files


def main() -> None:
    root = Tk()
    
    root.title("Battleship")
    root.resizable(False, False)

    controller = GameController(root)
    controller.start()

    root.mainloop()


if __name__ == "__main__":
    main()