#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

import operator
from itertools import product
from functools import reduce
from typing import NamedTuple

# Input Parse
puzzle = AdventOfCode(year=2021, day=9)
puzzle_input = puzzle.get_input()


smoke_flow_model = list(map(lambda x: list(map(int, list(x))), puzzle_input))

class Position(NamedTuple):
    row: int = 0
    col: int = 0

    def __add__(self, other):
        return Position(*map(sum, zip(self, other)))

# Actual Code
result = puzzle_input
low_points = []
directions = {Position(1, 0), Position(0, 1), Position(-1, 0), Position(0, -1)}
def in_bounds(pos):
    if 0 <= pos.row < len(smoke_flow_model):
        if 0 <= pos.col < len(smoke_flow_model[0]):
            return True
    return False

def get_basin(low_point):
    frontier = set([low_point])
    basin = set()
    while frontier:
        pos = frontier.pop()
        neighbours = {pos + dir for dir in directions if in_bounds(pos + dir)}
        neighbours = set(filter(lambda n: n not in (basin|frontier) and smoke_flow_model[n.row][n.col] != 9, neighbours))
        frontier |= neighbours
        basin.add(pos)
    return basin



basin_sizes = list()
for pos  in product(range(len(smoke_flow_model)), range(len(smoke_flow_model[0]))):
    pos = Position(*pos)
    value = smoke_flow_model[pos.row][pos.col]
    neighbours = {pos + dir for dir in directions if in_bounds(pos + dir)}
    is_low_point =  not tuple(filter(lambda n: smoke_flow_model[n.row][n.col] <= value, neighbours))
    if is_low_point:
        basin = get_basin(pos)
        basin_sizes.append(len(basin))


# Result
print(reduce(operator.mul, list(sorted(basin_sizes, reverse=True))[:3]))
