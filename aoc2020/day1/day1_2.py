#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path

from requests import exceptions
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode
from itertools import combinations
from operator import mul
from functools import reduce

# Input Parse
puzzle = AdventOfCode(year=2020, day=1)
puzzle_input = puzzle.get_input()

expenses = map(int, puzzle_input)
DESIRED_SUM = 2020

# Actual Code
seen = set()

for expense_candidates in combinations(expenses, 3):
    if sum(expense_candidates) == DESIRED_SUM:
        print(f"Product of entries is {reduce(mul, expense_candidates)}")
        break

# Result
# print(result)