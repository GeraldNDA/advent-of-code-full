#!/usr/bin/env python3
# Add current dir to path
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, starmap
from math import comb, copysign
from math import gcd
from operator import methodcaller
import sys
from pathlib import Path
from typing import NamedTuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=5)
puzzle_input = puzzle.get_input()

def sign(x):
    return int(copysign(1.0, x))

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(*map(sum, zip(self, other)))

class Line:
    def __init__(self, start, end) -> None:
        self.start = min(start, end, key=sum)
        self.end = max(end, start, key=sum)

    def is_straight(self) -> bool:
        return self.is_horizontal() or self.is_vertical()
    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def __iter__(self):
        vert = self.end.y - self.start.y
        horiz = self.end.x - self.start.x
        divider = gcd(vert, horiz)
        slope = Point(horiz//divider, vert//divider)
        assert abs(slope.x) in (1, 0)
        assert abs(slope.y) in (1, 0)

        start = self.start
        print(slope, start, self.end)
        while start != self.end:
            yield start
            start += slope
        yield start

    @staticmethod
    def parse(line_str):
        points_str = map(methodcaller("split", ","), line_str.split(" -> "))
        points = (Point(*map(int, p)) for p in points_str)
        return Line(*points)
# Actual Code
point_map = defaultdict(int)
lines = filter(methodcaller("is_straight"), map(Line.parse, puzzle_input))
for line in lines:
    for p in line:
        point_map[p] += 1

# Result
print(sum(1 for _, crossings in point_map.items() if crossings > 1))
# print(len(point_map))