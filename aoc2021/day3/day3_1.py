#!/usr/bin/env python3
# Add current dir to path
from operator import itemgetter
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=3)
puzzle_input = puzzle.get_input()

diag_report = puzzle_input
# Actual Code
gamma_rate = ""
epsilon_rate = ""

rate_size = len(diag_report[0])
for i in range(rate_size):
    getter = itemgetter(i)
    rate_at = list(map(getter, diag_report))
    gamma_rate += max("01", key=lambda b: rate_at.count(b))
    epsilon_rate += min("01", key=lambda b: rate_at.count(b))


# Result
print(int(gamma_rate, 2)*int(epsilon_rate, 2))