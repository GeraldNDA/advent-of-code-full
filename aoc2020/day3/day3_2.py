#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import count
from functools import reduce
from operator import mul

# Input Parse
puzzle = AdventOfCode(year=2020, day=3)
puzzle_input = puzzle.get_input()

class GridIndex:
    row: int
    col: int

class TreeGrid:
    TREE = "#"
    EMPTY = "."

    def __init__(self, trees) -> None:
        self.trees = trees
        self.rows = len(trees)

    def __getitem__(self, indicies):
        row, col = indicies
        return self.trees[row][col % len(self.trees[row])]

area = TreeGrid(puzzle_input)
slopes = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
]
# Actual Code
slope_to_tree_count = lambda rstep, cstep: sum(1 for idx in zip(range(0, area.rows, rstep), count(step=cstep)) if area[idx] == TreeGrid.TREE)
print(reduce(mul, map(lambda idx: slope_to_tree_count(idx[0], idx[1]), slopes)))


# Result
# print(tree_count)