#!/usr/bin/env python3
# Add current dir to path
from ctypes import Union
from enum import Enum
import sys
from pathlib import Path
from typing import NamedTuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=2)
puzzle_input = puzzle.get_input()

class Position(NamedTuple):
    hpos: int = 0
    depth: int = 0

    def __add__(self, other: "Position") -> "Position":
        assert isinstance(other, Position)
        return Position(self.hpos+other.hpos, self.depth+other.depth)

    def __mul__(self, other:int) -> "Position":
        assert isinstance(other, int)
        return Position(self.hpos*other, self.depth*other)

class Direction(Enum):
    up = Position(depth=-1)
    down = Position(depth=+1)
    forward = Position(hpos=+1)

horizontal_aim = Position(hpos=1)
aim = Position()
curr_pos = Position()
for instr in puzzle_input:
    command, amount = instr.split(" ")
    amount = int(amount)
    command = Direction[command]
    if command is Direction.forward:
        curr_pos += horizontal_aim*amount
        curr_pos += aim*amount
    else:
        aim += command.value*amount

# Result
print(curr_pos.hpos * curr_pos.depth)