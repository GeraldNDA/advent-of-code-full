#!/usr/bin/env python3
# Add current dir to path
from itertools import product
import sys
from pathlib import Path
from typing import NamedTuple, Tuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from mapping import Point, CardinalDirections as Directions
from operator import methodcaller
# Input Parse
puzzle = AdventOfCode(year=2021, day=15)
puzzle_input = puzzle.get_input()

chiton_risk_map = {}
goal = Point(0, 0)
for ridx, row in enumerate(puzzle_input):
    for cidx, risk in enumerate(row):
        goal = Point(ridx, cidx)
        chiton_risk_map[goal] = int(risk)

class Path(NamedTuple):
    risk_level: int = 0
    path: Tuple[Point] = tuple()

    def add_point(self, point):
        return Path(risk_level=self.risk_level + chiton_risk_map[point], path=self.path+(point,))

    def last_point(self):
        assert self.path
        return self.path[-1]

    def risk_estimate(self, goal):
        assert self.path
        # Lowest possible risk = 1
        return self.remaining_distance_estimate(goal)*1 + self.risk_level
    
    def remaining_distance_estimate(self, goal):
        assert self.path
        return sum(goal-self.last_point())

    def __contains__(self, point: Point) -> bool:
        return point in self.path

total_risk = sum(r for p,r in chiton_risk_map.items() if p.x == 0 or p.y == goal.y)
# Actual Code
# Result
wave_front = [Path(path=(Point(0, 0),))]
seen = set()
done = False
while not done:
    curr_path = wave_front.pop(0)
    if curr_path.last_point() in seen:
        continue
    seen.add(curr_path.last_point())

    if curr_path.last_point() == goal:
        print(curr_path.risk_level)
        break

    last_point = curr_path.last_point()
    risk_levels = {last_point+d: chiton_risk_map[last_point+d] for d in Directions if last_point+d in chiton_risk_map and last_point+d not in seen}
    for next_point, _ in risk_levels.items():
        wave_front.append(curr_path.add_point(next_point))

    wave_front.sort(key=methodcaller("risk_estimate", goal))


