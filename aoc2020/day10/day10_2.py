#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from functools import lru_cache
# Input Parse
puzzle = AdventOfCode(year=2020, day=10)
puzzle_input = puzzle.get_input()
jolt_adapters = [0] + list(sorted(map(int, puzzle_input)))
jolt_adapters.append(3 + max(jolt_adapters))

#would've just used @cache, but I'm using 3.8 lol
# @lru_cache(maxsize=None)
def num_combinations_after(adapters, start_idx=0):
    if start_idx == len(adapters) - 1:
        return 1
    num_arrangements = 0
    other_indexes = {
        min(start_idx+1, len(adapters)-1), 
        min(start_idx+2, len(adapters)-1), 
        min(start_idx+3, len(adapters)-1)
    }
    # print(other_indexes)

    return sum(
        map(
            lambda idx: num_combinations_after(adapters, start_idx=idx),
            filter(lambda other_idx: 0 < adapters[other_idx] - adapters[start_idx] <= 3, other_indexes)
        )
    )

print(num_combinations_after(tuple(jolt_adapters)))