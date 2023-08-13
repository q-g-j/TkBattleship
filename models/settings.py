class Settings:
    def __init__(self, cell_size: int = 40, theme: str = "classic") -> None:
        self.cell_size = cell_size
        self.theme = theme

    def to_dict(self):
        return {"cell_size": self.cell_size, "theme": self.theme}
