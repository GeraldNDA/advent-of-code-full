#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import chain

# Input Parse
puzzle = AdventOfCode(year=2021, day=6)
puzzle_input = puzzle.get_input()

class LanternFish:
    def __init__(self, starting_day) -> None:
        self.timer = starting_day

    def tick(self):
        if not self.timer:
            self.timer = 6
            return (self, LanternFish(8))
        self.timer -= 1
        return (self,)

# Actual Code
school = map(LanternFish, map(int, puzzle_input.split(",")))
for i in range(80):
    print(i)
    school = chain(*(fish.tick() for fish in school))

# Result
print(len(tuple(school)))