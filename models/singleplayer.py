import random

from models.enums import Event, Side, Orientation
from models.position import Position
from models.validator import Validator
from events.eventaggregator import EventAggregator
from services.injector import inject


@inject(EventAggregator, Validator)
class SinglePlayer:
    def __init__(
            self, event_aggregator: EventAggregator, validator: Validator
    ) -> None:
        self.__event_aggregator = event_aggregator
        self.__validator = validator

        self.__ai_all_positions_to_try: list[Position] = []

        self.__ai_last_hit_positions: list[Position] = []
        self.__ai_last_hit_possible_new_positions: list[Position] = []
        self.__ai_last_hit_ship_orientation: Orientation = Orientation.NONE

    def __ai_place_mark(self, pos: Position):
        self.__ai_last_hit_positions.append(pos)

        self.__event_aggregator.publish(Event.SHIP_HIT, Side.LEFT, pos)

        if self.__validator.is_ship_destroyed_at_position(Side.LEFT, pos):
            self.__ai_exclude_from_list_if_ship_destroyed()
            self.__reset_for_destroyed_ship()

    def __ai_exclude_from_list_if_ship_destroyed(self):
        for pos in self.__ai_last_hit_positions:
            adjacent_free_positions = self.__validator.get_adjacent_positions_nwse(pos)
            for adj_free_pos in adjacent_free_positions:
                if adj_free_pos in self.__ai_all_positions_to_try:
                    self.__ai_all_positions_to_try.remove(adj_free_pos)

    def __ai_try_random_position(self):
        random_pos = random.choice(self.__ai_all_positions_to_try)

        self.__ai_all_positions_to_try.remove(random_pos)

        if not self.__validator.is_cell_empty(Side.LEFT, random_pos):
            self.__ai_place_mark(random_pos)

    def __ai_try_adjacent_position(self):
        num_last_hit_positions = len(self.__ai_last_hit_positions)

        # try an adjacent position:
        if num_last_hit_positions == 1:
            if len(self.__ai_last_hit_possible_new_positions) == 0:
                self.__ai_last_hit_possible_new_positions = self.__validator.get_adjacent_positions_nwse(
                    self.__ai_last_hit_positions[0], self.__ai_all_positions_to_try)

            adj_pos = random.choice(self.__ai_last_hit_possible_new_positions)

            self.__ai_all_positions_to_try.remove(adj_pos)

            self.__ai_last_hit_possible_new_positions.remove(adj_pos)

            if not self.__validator.is_cell_empty(Side.LEFT, adj_pos):
                self.__ai_place_mark(adj_pos)

            return

        if num_last_hit_positions == 2:
            self.__ai_last_hit_possible_new_positions.clear()
            self.__ai_last_hit_ship_orientation = self.__validator.get_ship_orientation_from_positions(
                self.__ai_last_hit_positions[0], self.__ai_last_hit_positions[1])

        if len(self.__ai_last_hit_possible_new_positions) == 0:
            if self.__ai_last_hit_ship_orientation == Orientation.HORIZONTAL:
                left_pos, right_pos = Position.get_left_and_right(self.__ai_last_hit_positions[0],
                                                                  self.__ai_last_hit_positions[1])

                # look for possible positions to the right:
                for col in range(right_pos.col + 1, 10):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(right_pos.row, col)
                    if pos in self.__ai_all_positions_to_try:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

                # look for possible positions to the left:
                for col in reversed(range(left_pos.col)):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(left_pos.row, col)
                    if pos in self.__ai_all_positions_to_try:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

            elif self.__ai_last_hit_ship_orientation == Orientation.VERTICAL:
                top_pos, bottom_pos = Position.get_top_and_bottom(self.__ai_last_hit_positions[0],
                                                                  self.__ai_last_hit_positions[1])

                # look for possible positions below:
                for row in range(bottom_pos.row + 1, 10):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(row, bottom_pos.col)
                    if pos in self.__ai_all_positions_to_try:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

                # look for possible positions up:
                for row in reversed(range(top_pos.row)):
                    if len(self.__ai_last_hit_possible_new_positions) == 8:
                        break
                    pos = Position(row, top_pos.col)
                    if pos in self.__ai_all_positions_to_try:
                        self.__ai_last_hit_possible_new_positions.append(pos)
                    else:
                        break

        adj_pos: Position | None = None
        do_try = True
        for pos in self.__ai_last_hit_possible_new_positions:
            if not do_try:
                break
            for hit_pos in self.__ai_last_hit_positions:
                if pos.row == hit_pos.row + 1 or \
                        pos.row == hit_pos.row - 1 or \
                        pos.col == hit_pos.col + 1 or \
                        pos.col == hit_pos.col - 1:
                    adj_pos = pos
                    do_try = False
                    break

        self.__ai_all_positions_to_try.remove(adj_pos)
        self.__ai_last_hit_possible_new_positions.remove(adj_pos)

        if not self.__validator.is_cell_empty(Side.LEFT, adj_pos):
            self.__ai_place_mark(adj_pos)

        return

    def __reset_for_destroyed_ship(self):
        self.__ai_last_hit_positions.clear()
        self.__ai_last_hit_possible_new_positions.clear()
        self.__ai_last_hit_ship_orientation = Orientation.NONE

    def ai_make_move(self) -> None:
        num_last_hit_positions = len(self.__ai_last_hit_positions)

        # if nothing was hit at the last move:
        if num_last_hit_positions == 0:
            # try a random position:
            self.__ai_try_random_position()

        # if there are tracked hit positions:
        else:
            # try an adjacent position next:
            self.__ai_try_adjacent_position()

    def ai_reset_for_new_game(self):
        self.__ai_all_positions_to_try.clear()
        for row in range(10):
            for col in range(10):
                pos = Position(row, col)
                if pos not in self.__ai_all_positions_to_try:
                    self.__ai_all_positions_to_try.append(Position(row, col))
        self.__reset_for_destroyed_ship()
