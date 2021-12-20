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
    filter(lambda d: d > 0, map(lambda depth_pair: depth_pair[1]-depth_pair[0], 
        zip(depth_measurements[:-1], depth_measurements[1:])
    ))
))

# Result
print(increasing_depths)