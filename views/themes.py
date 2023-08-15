from ttkthemes.themed_tk import ThemedTk


class Themes:
    ALL_THEMES: list[str] = []

    @staticmethod
    def init(root: ThemedTk):
        available_themes = root.get_themes()

        # I picked a few themes from ttkthemes that actually work with this app:
        picked_themes = [
            "adapta",
            "alt",
            "arc",
            "clam",
            "default",
            "elegance",
            "keramik",
            "plastik",
            "scidblue",
            "scidgreen",
            "scidgrey",
            "scidmint",
            "scidpink",
            "scidpurple",
            "scidsand",
            "vista",
            "winnative",
            "winxpblue",
            "xpnative",
            "yaru"
        ]

        Themes.ALL_THEMES = sorted(
            [theme for theme in picked_themes if theme in available_themes or theme == "default"])
