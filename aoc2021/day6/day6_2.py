#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from functools import lru_cache

# Input Parse
puzzle = AdventOfCode(year=2021, day=6)
puzzle_input = puzzle.get_input()

original_school = map(int, puzzle_input.split(","))


# Actual Code
@lru_cache(256)
def lantern_children(start, num_days):
    children = 0
    internal_timer = start

    if num_days >= start + 1:
        num_days -= start + 1
        children += 1 + lantern_children(8, num_days)
        internal_timer = 6

    if num_days > internal_timer:
        while num_days >= 7:
            num_days -= 7
            children += 1 + lantern_children(8, num_days)
            internal_timer = 6
    internal_timer -= num_days

    return children


# Result
final_school_size = sum(1 + lantern_children(s, 256) for s in original_school)
print(final_school_size)