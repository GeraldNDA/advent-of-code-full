#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=7)
puzzle_input = puzzle.get_input()

# Actual Code
crab_positions = tuple(map(int, puzzle_input.split(",")))

def triangle_num(x):
    return (x * (x+1)) // 2

# Result
dist = float("inf")
for base_pos in range(min(crab_positions), max(crab_positions)):
    dist = min(dist, sum(triangle_num(abs(pos - base_pos)) for pos in crab_positions))
print(dist)