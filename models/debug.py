class Debug:
    PLAYER_PLACE_RANDOM_SHIPS = True

    @staticmethod
    def print_playing_field(playing_field: list) -> None:
        print()
        for row in range(10):
            print("|", end="")
            for column in range(10):
                print("{0}|".format(playing_field[row][column]), end="")
            print()
