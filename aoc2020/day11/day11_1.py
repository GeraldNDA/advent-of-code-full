#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode
from mapping import OrdinalDirections, Point

from enum import Enum
from operator import methodcaller
# Input Parse
puzzle = AdventOfCode(year=2020, day=11)
puzzle_input = puzzle.get_input()

# Actual Code
class SeatState(Enum):
    OCCUPIED = "#"
    EMPTY = "L"
    FLOOR = "."

class SeatPosition:
    def __init__(self, state) -> None:
        self.state = state
        self.next_state = state
        self.neighbours = set()

    def add_neighbour(self, position):
        self.neighbours.add(position)

    def get_next_state(self):
        num_occupied = sum(1 for neighbour in self.neighbours if neighbour.state is SeatState.OCCUPIED)
        if num_occupied == 0 and self.state is SeatState.EMPTY:
            self.next_state = SeatState.OCCUPIED
        elif num_occupied >= 4 and self.state is SeatState.OCCUPIED:
            self.next_state = SeatState.EMPTY
        else:
            self.next_state = self.state
            return False
        return True

    def apply_next_state(self):
        self.state = self.next_state


class SeatLayout:
    def __init__(self, layout):
        self.layout = layout

    def simulate(self):
        while any(set(map(methodcaller("get_next_state"), self.layout.values()))):
            for seat in self.layout.values():
                seat.apply_next_state()

    def __len__(self):
        # Number of occupied seats
        return sum(1 for seat in self.layout.values() if seat.state is SeatState.OCCUPIED)

    @staticmethod
    def parse_layout(layout_str):
        layout = dict()
        for ridx, row in enumerate(layout_str):
            for cidx, seat in enumerate(row):
                layout[Point(ridx, cidx)] = SeatPosition(SeatState(seat))

        for pos, seat in layout.items():
            for dir in OrdinalDirections:
                neighbour_pos = pos + dir.value
                if neighbour_pos in layout:
                    seat.add_neighbour(layout[neighbour_pos])

        return SeatLayout(layout)

seats = SeatLayout.parse_layout(puzzle_input)
seats.simulate()
print(len(seats))

# Result
