from PIL import Image, ImageTk
from ttkthemes import ThemedTk

from controllers.gamecontroller import GameController


def main() -> None:
    root = ThemedTk()

    controller = GameController(root)
    controller.start()

    root.mainloop()


if __name__ == "__main__":
    main()
