#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode
from mapping import CardinalDirections, Point

from enum import Enum
# Input Parse
puzzle = AdventOfCode(year=2020, day=12)
puzzle_input = puzzle.get_input()

# Actual Code
class TurnDirections(Enum):
    LEFT = Point(1, -1)
    RIGHT = Point(-1, 1)

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(other.y*self.value.x, other.x*self.value.y)

    def __radd__(self, other):
        return self + other


class NavAction(Enum):
    N = CardinalDirections.NORTH
    E = CardinalDirections.EAST
    S = CardinalDirections.SOUTH
    W = CardinalDirections.WEST
    L = TurnDirections.LEFT
    R = TurnDirections.RIGHT
    F = None

    @classmethod
    def from_command(self, command):
        return NavAction[command[0]], int(command[1:])

class Ship:
    def __init__(self) -> None:
        self.pos = Point(0, 0)
        self.waypoint = CardinalDirections.NORTH.value + 10*CardinalDirections.EAST.value
        self.dir = CardinalDirections.EAST.value
    
    def apply(self, command):
        action, value = NavAction.from_command(command)
        if action is NavAction.F:
            self.pos += self.waypoint*value
        elif action.value in CardinalDirections:
            self.waypoint += value*action.value
        elif action.value in TurnDirections:
            assert value % 90 == 0, (action, value)
            for _ in range(value // 90):
                self.waypoint += action.value

ship = Ship()
for command in puzzle_input:
    ship.apply(command)

# Result
print(sum(map(abs, ship.pos)))