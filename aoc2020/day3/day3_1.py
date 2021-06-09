#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import count

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

# Actual Code
tree_count = sum(1 for idx in zip(range(area.rows), count(step=3)) if area[idx] == TreeGrid.TREE)

# Result
print(tree_count)