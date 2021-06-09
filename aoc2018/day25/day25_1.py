#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=25)
puzzle_input = puzzle.get_input()

class Point():
    def __init__(self, coords):
        self.coords = tuple(coords)
        self.dims = len(self.coords)

    def manhattan_distance(self, other_point):
        return sum(
            abs(self.coords[i] - other_point.coords[i])
            for i in range(self.dims)
        )

    @staticmethod
    def parse(point_info):
        return Point(map(int, point_info.split(",")))

stars = tuple(map(Point.parse, puzzle_input))
constellations = []
for curr_star in stars:
    closest_constellations = set()
    for idx, constellation in enumerate(constellations):
        if any(curr_star.manhattan_distance(star) <= 3 for star in constellation):
            closest_constellations.add(idx)
    
    last_constellation = set()
    for idx in reversed(sorted(closest_constellations)):
        last_constellation |= constellations.pop(idx)
    constellations.append(last_constellation | {curr_star,})
# Actual Code
# print(constellations)
# Result
print(len(constellations))