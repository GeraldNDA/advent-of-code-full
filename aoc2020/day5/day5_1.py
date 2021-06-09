#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from typing import NamedTuple

# Input Parse
puzzle = AdventOfCode(year=2020, day=5)
puzzle_input = puzzle.get_input()

class SeatRange(NamedTuple):
    min_seat: int
    max_seat: int

    def upper(self):
        size = self.max_seat - self.min_seat + 1
        return SeatRange(self.min_seat + size//2, self.max_seat)

    def lower(self):
        size = self.max_seat - self.min_seat + 1
        return SeatRange(self.min_seat, self.max_seat - size//2)
    
    def as_single(self):
        return self.max_seat if self.max_seat == self.min_seat else None




# Actual Code
def to_seat_id(boarding_pass):
    row = SeatRange(0, 127)
    col = SeatRange(0, 7)

    apply_pass = {
        "F": lambda: (row.lower(), col),
        "B": lambda: (row.upper(), col),
        "L": lambda: (row, col.lower()),
        "R": lambda: (row, col.upper()),
    }

    for char in boarding_pass:
        row, col = apply_pass[char]()

    row_id, col_id = row.as_single(), col.as_single()
    assert row_id is not None and col_id is not None, f"{row} {col} {boarding_pass}"
    return row_id*8 + col_id

# Result
print(to_seat_id("BFFFBBFRRR"))
print(max(map(to_seat_id, puzzle_input)))