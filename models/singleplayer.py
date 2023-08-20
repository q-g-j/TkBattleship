import random

from events.eventaggregator import EventAggregator
from models.enums import Event, Side, Orientation, CellContent, ShipTypes
from models.position import Position
from models.validator import Validator
from services.injector import inject
from utils.sleep import threaded_sleep
from views.images import Images


@inject(EventAggregator, Validator)
class SinglePlayer:
    def __init__(self, event_aggregator: EventAggregator, validator: Validator) -> None:
        self.__event_aggregator = event_aggregator
        self.__validator = validator

        self.__ai_all_positions_to_try: list[Position] = []
        self.__ai_all_positions_to_try_full: list[Position] = []

        self.__ai_last_hit_positions: list[Position] = []
        self.__ai_last_hit_possible_new_positions: list[Position] = []
        self.__ai_last_hit_ship_orientation: Orientation = Orientation.NONE
        self.__ai_all_hit_positions: list[Position] = []
        self.__ai_all_ship_lengths: list[int] = []

        for ship_type in ShipTypes:
            for _ in range(ship_type[2]):
                self.__ai_all_ship_lengths.append(ship_type[1])

        for row in range(10):
            for col in range(10):
                pos = Position(row, col)
                if col % 2 != 0 and row % 2 != 0:
                    self.__ai_all_positions_to_try.append(pos)
                elif col % 2 == 0 and row % 2 == 0:
                    self.__ai_all_positions_to_try.append(pos)

        for row in range(10):
            for col in range(10):
                self.__ai_all_positions_to_try_full.append(Position(row, col))

    def __ai_place_mark(self, pos: Position) -> None:
        self.__ai_last_hit_positions.append(pos)
        self.__ai_all_hit_positions.append(pos)

        self.__event_aggregator.publish(Event.SHIP_HIT, Side.LEFT, pos)

        if self.__validator.is_ship_destroyed_at_position(Side.LEFT, pos):
            if len(self.__ai_all_ship_lengths) != 1:
                self.__ai_all_ship_lengths.remove(len(self.__ai_last_hit_positions))
                self.__ai_exclude_from_list_if_ship_destroyed()
                self.__ai_exclude_from_list_if_remaining_ships_dont_fit()
                self.__reset_for_destroyed_ship()

    def __ai_exclude_from_list_if_remaining_ships_dont_fit(self):
        playing_field = []
        for row in range(10):
            inner_list = []
            for col in range(10):
                p = Position(row, col)
                if p in self.__ai_all_hit_positions:
                    inner_list.append(CellContent.FILLED)
                else:
                    inner_list.append(CellContent.EMPTY)
            playing_field.append(inner_list)

        for p in self.__ai_all_positions_to_try:
            does_any_length_fit = False
            for length in self.__ai_all_ship_lengths:
                orientation = self.__validator.does_ship_fit_at_position(Side.LEFT, p, length, playing_field)
                if orientation != Orientation.NONE:
                    does_any_length_fit = True
                    break
            if not does_any_length_fit:
                self.__ai_all_positions_to_try_full.remove(p)
                self.__ai_all_positions_to_try.remove(p)

    def __ai_exclude_from_list_if_ship_destroyed(self) -> None:
        for pos in self.__ai_last_hit_positions:
            adjacent_free_positions = self.__validator.get_adjacent_positions(pos)
            for adj_free_pos in adjacent_free_positions:
                if adj_free_pos in self.__ai_all_positions_to_try:
                    self.__ai_all_positions_to_try.remove(adj_free_pos)
                if adj_free_pos in self.__ai_all_positions_to_try_full:
                    self.__ai_all_positions_to_try_full.remove(adj_free_pos)

    def __ai_try_random_position(self) -> tuple[bool, Position | None]:
        random_pos = random.choice(self.__ai_all_positions_to_try)

        self.__ai_all_positions_to_try.remove(random_pos)
        self.__ai_all_positions_to_try_full.remove(random_pos)

        if not self.__validator.is_cell_empty(Side.LEFT, random_pos):
            self.__ai_place_mark(random_pos)
            return True, random_pos

        return False, random_pos

    def __ai_try_adjacent_position(self) -> tuple[bool, Position | None]:
        num_last_hit_positions = len(self.__ai_last_hit_positions)

        # try an adjacent position:
        if num_last_hit_positions == 1:
            if len(self.__ai_last_hit_possible_new_positions) == 0:
                self.__ai_last_hit_possible_new_positions = self.__validator.get_adjacent_positions_nwse(
                    self.__ai_last_hit_positions[0], self.__ai_all_positions_to_try_full
                )

            adj_pos = random.choice(self.__ai_last_hit_possible_new_positions)

            if adj_pos in self.__ai_all_positions_to_try:
                self.__ai_all_positions_to_try.remove(adj_pos)
            self.__ai_all_positions_to_try_full.remove(adj_pos)

            self.__ai_last_hit_possible_new_positions.remove(adj_pos)

            if not self.__validator.is_cell_empty(Side.LEFT, adj_pos):
                self.__ai_place_mark(adj_pos)
                return True, adj_pos

            return False, adj_pos

        if num_last_hit_positions == 2:
            self.__ai_last_hit_possible_new_positions.clear()
            self.__ai_last_hit_ship_orientation = self.__validator.get_ship_orientation_from_positions(
                self.__ai_last_hit_positions[0], self.__ai_last_hit_positions[1]
            )

        if len(self.__ai_last_hit_possible_new_positions) == 0:
            if self.__ai_last_hit_ship_orientation == Orientation.HORIZONTAL:
                left_pos, right_pos = Position.get_left_and_right(
                    self.__ai_last_hit_positions[0], self.__ai_last_hit_positions[1]
                )

                # look for possible positions to the right:
                for col in range(right_pos.col + 1, 10):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(right_pos.row, col)
                    if pos in self.__ai_all_positions_to_try_full:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

                # look for possible positions to the left:
                for col in reversed(range(left_pos.col)):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(left_pos.row, col)
                    if pos in self.__ai_all_positions_to_try_full:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

            elif self.__ai_last_hit_ship_orientation == Orientation.VERTICAL:
                top_pos, bottom_pos = Position.get_top_and_bottom(
                    self.__ai_last_hit_positions[0], self.__ai_last_hit_positions[1]
                )

                # look for possible positions below:
                for row in range(bottom_pos.row + 1, 10):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(row, bottom_pos.col)
                    if pos in self.__ai_all_positions_to_try_full:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

                # look for possible positions up:
                for row in reversed(range(top_pos.row)):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(row, top_pos.col)
                    if pos in self.__ai_all_positions_to_try_full:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

        adj_pos: Position | None = None
        do_try = True
        for pos in self.__ai_last_hit_possible_new_positions:
            if not do_try:
                break
            for hit_pos in self.__ai_last_hit_positions:
                if (
                        pos.row == hit_pos.row + 1
                        or pos.row == hit_pos.row - 1
                        or pos.col == hit_pos.col + 1
                        or pos.col == hit_pos.col - 1
                ):
                    adj_pos = pos
                    do_try = False
                    break

        if adj_pos in self.__ai_all_positions_to_try:
            self.__ai_all_positions_to_try.remove(adj_pos)
        self.__ai_all_positions_to_try_full.remove(adj_pos)
        self.__ai_last_hit_possible_new_positions.remove(adj_pos)

        if not self.__validator.is_cell_empty(Side.LEFT, adj_pos):
            self.__ai_place_mark(adj_pos)
            return True, adj_pos

        return False, adj_pos

    def __reset_for_destroyed_ship(self) -> None:
        self.__ai_last_hit_positions.clear()
        self.__ai_last_hit_possible_new_positions.clear()
        self.__ai_last_hit_ship_orientation = Orientation.NONE

    def ai_make_move(self) -> None:
        num_last_hit_positions = len(self.__ai_last_hit_positions)

        # if nothing was hit at the last move:
        if num_last_hit_positions == 0:
            # try a random position:
            has_hit, pos = self.__ai_try_random_position()

        # if there are tracked hit positions:
        else:
            # try an adjacent position next:
            has_hit, pos = self.__ai_try_adjacent_position()

        if not has_hit:
            self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, pos, Images.SPLASH)

            def clear_image():
                self.__event_aggregator.publish(Event.CELL_IMAGE_SET, Side.LEFT, pos, Images.EMPTY)

            threaded_sleep(clear_image, 0.5)
