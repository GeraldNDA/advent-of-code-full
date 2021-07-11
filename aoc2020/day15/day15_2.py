#!/usr/bin/env python3
# Add current dir to path
from collections import defaultdict
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=15)
puzzle_input = puzzle.get_input()

STARTING_NUMBERS = tuple(map(int, puzzle_input.split(",")))
# STARTING_NUMBERS = (0, 3, 6)
MAX_NUMBER = 30000000

# Actual Code
when_spoken = defaultdict(int)
last_spoken = None
for idx in range(MAX_NUMBER):
    if idx in range(len(STARTING_NUMBERS)):
        last_spoken = STARTING_NUMBERS[idx]
        when_spoken[STARTING_NUMBERS[idx]] = idx
    else:
        num = 0
        if last_spoken in when_spoken:
            num = idx - when_spoken[last_spoken] - 1
        when_spoken[last_spoken], last_spoken = idx-1, num
    # print(last_spoken)

# Result
print(last_spoken)