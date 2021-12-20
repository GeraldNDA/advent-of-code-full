#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode
from statistics import median

# Input Parse
puzzle = AdventOfCode(year=2021, day=7)
puzzle_input = puzzle.get_input()

# Actual Code
crab_positions = tuple(map(int, puzzle_input.split(",")))
base_pos = int(median(crab_positions))

# Result
print(sum(abs(pos - base_pos) for pos in crab_positions))