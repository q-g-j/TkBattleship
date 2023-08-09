class Position:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.col = column
        self.column = column
        self.x = column
        self.y = row

    def __eq__(self, other):
        return True if self.row == other.row and self.col == other.col else False
