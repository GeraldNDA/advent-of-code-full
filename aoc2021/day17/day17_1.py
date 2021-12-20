#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
from typing import NamedTuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import count
from math import sqrt
from mapping import Point
import re
# Input Parse
puzzle = AdventOfCode(year=2021, day=17)
puzzle_input = puzzle.get_input()

puzzle_input = "target area: x=20..30, y=-10..-5"

TARGET_AREA_PARSER = re.compile(r"target area: x=(?P<start_x>-?\d+)\.\.(?P<end_x>-?\d+), y=(?P<start_y>-?\d+)\.\.(?P<end_y>-?\d+)")
class TargetArea(NamedTuple):
    start: Point
    end: Point

    @staticmethod
    def parse(target_area_str):
        res = TARGET_AREA_PARSER.match(target_area_str)
        assert res is not None
        return TargetArea(
            start=Point(int(res["start_x"]), int(res["start_y"])),
            end=Point(int(res["end_x"]), int(res["end_y"]))
        )

    def __contains__(self, p: Point) -> bool:
        return (self.start.x <= p.x <= self.end.x) and (self.start.y <= p.y <= self.end.y)


# need to find an horizontal velocity that resets to zero above the area
# end_x = (start_x_velocity-1)+ (start_x_velocity-2)+ ... 0
# end_x = start_x_velocity*(start_x_velocity+1)//2
# end_x*2 = start_x_velocity**2 + start_velocity
# a = 1, b=1, c=-end_x*2
# start_x_velocity = -1/2 + sqrt(1 + 8*end_x)/2
def get_min_xvel(target_area):
    xvel = int(-0.5 + sqrt(1 + 8*target_area.end.x)/2)
    assert target_area.start.x <= sum(range(xvel))+xvel <= target_area.end.x
    return xvel

# Actually horizontal velocity doesn't matter for P1
# The probe will go up and then go back to y=0, from there, we want to increase it to reach the bottom of the target
# so yvel+1 = end_y
# to maximize this value, this should be a single step, so just use this formula as is 
def get_max_yvel(target_area):
    return abs(target_area.start.y)-1
# max_height = yvel*(yvel-1)//2
# if (n - end_y) == n - yvel*(yvel-1)//2

def test_start_vel(start_vel, target_area):
    pos = Point(0, 0)
    vel = start_vel
    while pos.x <= target_area.end.x and pos.y >= target_area.end.y:
        pos = pos + vel
        xdir = +1 if vel.x < 0 else (0 if vel.x == 0 else -1)
        vel = Point(x=vel.x + xdir, y=vel.y-1)
        if pos in target_area:
            return True
    return False

def max_height(start_vel):
    return ((start_vel.y)*(start_vel.y+1))//2

# end_y = 0+n*vy_s - (n^2+n)
# n = ? vy_s = ?

# end_x - start_x = n


# Actual Code
target = TargetArea.parse(puzzle_input)
vel = Point(get_min_xvel(target), get_max_yvel(target))

# Result
print(max_height(vel))