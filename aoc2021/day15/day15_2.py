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
from heapq import heappush, heappop
# Input Parse
puzzle = AdventOfCode(year=2021, day=15)
puzzle_input = puzzle.get_input()

chiton_risk_map = {}
goal = Point(0, 0)
for ridx, row in enumerate(puzzle_input):
    for cidx, risk in enumerate(row):
        goal = Point(ridx, cidx)
        chiton_risk_map[goal] = int(risk)
cave_dims = Point(len(puzzle_input), len(puzzle_input[0]))
for p, risk in tuple(chiton_risk_map.items()):
    for rmul in range(5):
        for cmul in range(5):
            chiton_risk_map[cave_dims*Point(rmul, cmul)+p] = ((risk-1)+ rmul + cmul) % 9 + 1

goal = Point(4,4)*cave_dims + goal


class Path(NamedTuple):
    risk_estimate: int = 0
    risk_level: int = 0
    path: Tuple[Point] = tuple()

    def add_point(self, point, goal):
        new_path = self.path + (point,)
        new_risk = self.risk_level + chiton_risk_map[point]
        return Path(risk_estimate=Path.estimate_risk(new_path, goal, new_risk), risk_level=new_risk, path=new_path)

    def last_point(self):
        assert self.path
        return self.path[-1]

    @staticmethod
    def estimate_risk(path, goal, curr_risk):
        assert path
        # Lowest possible risk = 1
        return Path.remaining_distance_estimate(path, goal)*1 + curr_risk
    
    @staticmethod
    def remaining_distance_estimate(path, goal):
        assert path
        return sum(goal-path[-1])

    def __contains__(self, point: Point) -> bool:
        return point in self.path

total_risk = sum(r for p,r in chiton_risk_map.items() if p.x == 0 or p.y == goal.y)
# Actual Code
# Result
wave_front = []
heappush(wave_front, Path(path=(Point(0, 0),)))
seen = set()
done = False
while not done:
    
    curr_path = heappop(wave_front)
    if curr_path.last_point() in seen:
        continue
    seen.add(curr_path.last_point())

    if curr_path.last_point() == goal:
        print(curr_path.risk_level)
        break

    last_point = curr_path.last_point()
    risk_levels = {last_point+d: chiton_risk_map[last_point+d] for d in Directions if last_point+d in chiton_risk_map and last_point+d not in seen}
    for next_point, _ in risk_levels.items():
        heappush(wave_front, curr_path.add_point(next_point, goal))


