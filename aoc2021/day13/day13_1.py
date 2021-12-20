#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
from typing import NamedTuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

import operator
from itertools import cycle


# Input Parse
puzzle = AdventOfCode(year=2021, day=13)
puzzle_input = puzzle.get_input()


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(*map(sum, zip(self, other)))
        if isinstance(other, int):
            return Point(*map(sum, zip(self, cycle([other]))))

    def __neg__(self):
        return Point(*map(operator.neg, self))

    def __sub__(self, other):
        return self + (-other)

    @classmethod
    def from_str(cls, point_str):
        return cls(*map(int, point_str.split(",")))

    def __str__(self):
        return f"Point({self.x},{self.y})"


# Actual Code
dots = set()
dot_stream = iter(puzzle_input)
for dot in dot_stream:
    if not dot:
        break
    dots.add(Point.from_str(dot)) 

fold_stream = dot_stream
for fold in fold_stream:
    assert fold.startswith("fold along ")
    fold = fold[len("fold along "):]
    axis, pos = fold.split("=")
    pos = int(pos)

    folded_paper = set()
    for dot in dots:
        axis_value = getattr(dot, axis)
        if axis_value < pos:
            folded_paper.add(dot)
        else:
            assert axis_value != pos
            folded_paper.add(dot + Point(**{axis: 2*(pos-axis_value)}))
    dots = folded_paper

    break # Part 1

# Result
print(len(dots))