#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=1)
puzzle_input = puzzle.get_input()

# Actual Code
depth_measurements = list(map(int, puzzle_input))
increasing_depths = len(list(
    filter(lambda d: d > 0, map(lambda depths: sum(depths[1:])-sum(depths[:-1]), 
        zip(depth_measurements[:-3], depth_measurements[1:-2], depth_measurements[2:-1], depth_measurements[3:])
    ))
))

# Result
print(increasing_depths)