from PIL import Image, ImageTk

from utils.files import Files


class ImageFiles:
    EMPTY = Files.fixed_path("assets/images/empty.png")
    UNDAMAGED = Files.fixed_path("assets/images/undamaged.png")
    UNDAMAGED_BLUE = Files.fixed_path("assets/images/undamaged_blue.png")
    UNDAMAGED_RED = Files.fixed_path("assets/images/undamaged_red.png")
    UNDAMAGED_GREEN = Files.fixed_path("assets/images/undamaged_green.png")
    HIT = Files.fixed_path("assets/images/hit.png")
    DESTROYED = Files.fixed_path("assets/images/destroyed.png")
    SPLASH = Files.fixed_path("assets/images/splash.png")


class Images(object):
    EMPTY: ImageTk.PhotoImage = None
    UNDAMAGED: ImageTk.PhotoImage = None
    UNDAMAGED_BLUE: ImageTk.PhotoImage = None
    UNDAMAGED_RED: ImageTk.PhotoImage = None
    UNDAMAGED_GREEN: ImageTk.PhotoImage = None
    HIT: ImageTk.PhotoImage = None
    DESTROYED: ImageTk.PhotoImage = None
    SPLASH: ImageTk.PhotoImage = None

    @staticmethod
    def init() -> None:
        image_empty_pil: Image.Image = Image.open(ImageFiles.EMPTY)
        image_undamaged_pil: Image.Image = Image.open(ImageFiles.UNDAMAGED).resize((32, 32))
        image_undamaged_blue_pil: Image.Image = Image.open(ImageFiles.UNDAMAGED_BLUE).resize((32, 32))
        image_undamaged_red_pil: Image.Image = Image.open(ImageFiles.UNDAMAGED_RED).resize((32, 32))
        image_undamaged_green_pil: Image.Image = Image.open(ImageFiles.UNDAMAGED_GREEN).resize((32, 32))
        image_hit_pil: Image.Image = Image.open(ImageFiles.HIT).resize((25, 25))
        image_destroyed_pil: Image.Image = Image.open(ImageFiles.DESTROYED).resize((25, 25))
        image_splash_pil: Image.Image = Image.open(ImageFiles.SPLASH).resize((25, 25))

        Images.EMPTY = ImageTk.PhotoImage(image_empty_pil)
        Images.UNDAMAGED = ImageTk.PhotoImage(image_undamaged_pil)
        Images.UNDAMAGED_BLUE = ImageTk.PhotoImage(image_undamaged_blue_pil)
        Images.UNDAMAGED_RED = ImageTk.PhotoImage(image_undamaged_red_pil)
        Images.UNDAMAGED_GREEN = ImageTk.PhotoImage(image_undamaged_green_pil)
        Images.HIT = ImageTk.PhotoImage(image_hit_pil)
        Images.DESTROYED = ImageTk.PhotoImage(image_destroyed_pil)
        Images.SPLASH = ImageTk.PhotoImage(image_splash_pil)

    @staticmethod
    def resize_image(image, maxsize):
        r1 = image.size[0] / maxsize[0]  # width ratio
        r2 = image.size[1] / maxsize[1]  # height ratio
        ratio = max(r1, r2)
        newsize = (int(image.size[0] / ratio), int(image.size[1] / ratio))
        print(newsize)
        image = image.resize(newsize)
        return image
