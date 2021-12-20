#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
from typing import NamedTuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import count, product
from math import sqrt
from cmath import sqrt as csqrt
from mapping import Point
import re
# Input Parse
puzzle = AdventOfCode(year=2021, day=17)
puzzle_input = puzzle.get_input()

# puzzle_input = "target area: x=20..30, y=-10..-5"

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

    def targets(self):
        for p in product(range(self.start.x, self.end.x+1), range(self.start.y, self.end.y+1)):
            yield Point(*p)

def nat_roots(a, b, c):
    poly = lambda x: (a*x + b)*x + c
    discrim = b**2 - (4*a*c)
    bot_sol =  int(((-b-csqrt(discrim))/(2 * a)).real)
    top_sol =  int(((-b + csqrt(discrim))/(2 * a)).real)

    solutions = set()
    if poly(bot_sol) == 0 and bot_sol>0:
        solutions.add(bot_sol)
    if poly(top_sol) == 0 and top_sol>0:
        solutions.add(top_sol)
    return solutions

def get_valid_xvels(target_x, max_steps):
    #end_pos = n*xvel - n*(n-1)//2
    # n is divisible by end_pos, and is odd or n == even_xvel
    # end_pos + (n-1)//2
    # if max_steps == 1:
    #     yield target_x 

    # if target_x % 2 == 1 and int(sqrt(target_x))**2 == target_x:
    #     yield (target_x+1)//2

    xvel = int(-0.5 + sqrt(1 + 8*target_x)/2)
    if target_x == (xvel*(xvel+1))//2 and xvel < max_steps:
        yield xvel

    xvel = int(target_x/max_steps + (max_steps-1)/2)
    if xvel >= max_steps:
        if target_x == max_steps*xvel - ((max_steps)*(max_steps-1))//2:
            # print("X",target_x, xvel, max_steps)
            yield xvel






def get_valid_yvels(target_y):
    # find all functional downward slopes
    assert target_y < 0
    min_yvel, max_yvel = target_y, -(target_y+1)
    equiv_yvel = lambda v: v if v < 0 else -v-1

    for yvel in range(min_yvel, max_yvel+1):
        nsteps = nat_roots(-0.5, equiv_yvel(yvel)+0.5, -target_y)
        if not nsteps:
            continue
        assert len(nsteps) == 1, nsteps
        nsteps = nsteps.pop()
        if yvel >= 0:
            nsteps += yvel*2 + 1 # at zero, stall for a step
        # print(f"={yvel} {nsteps}")
        yield yvel, nsteps

def get_valid_vels(target):
    for yvel, nstep in get_valid_yvels(target.y):
        for xvel in get_valid_xvels(target.x, nstep):
            yield Point(xvel, yvel)

def test_start_vel(start_vel, target_area):
    pos = Point(0, 0)
    vel = start_vel
    while pos.x <= target_area.end.x and pos.y >= target_area.start.y:
        pos = pos + vel
        xdir = +1 if vel.x < 0 else (0 if vel.x == 0 else -1)
        vel = Point(x=vel.x + xdir, y=vel.y-1)
        if pos in target_area:
            return True
    return False

target_area = TargetArea.parse(puzzle_input)
velocities = set()
for target in target_area.targets():
    for vel in get_valid_vels(target):
        assert test_start_vel(vel, target_area)
        velocities.add(vel)
# print(velocities)
print(len(velocities))