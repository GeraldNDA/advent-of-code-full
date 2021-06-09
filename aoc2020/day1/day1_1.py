#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=1)
puzzle_input = puzzle.get_input()

expenses = map(int, puzzle_input)
DESIRED_SUM = 2020

# Actual Code
seen = set()

for expense in expenses:
    other_expense = DESIRED_SUM - expense
    if other_expense not in seen:
        seen.add(expense)
    else:
        print(f"Product of entries is {expense*other_expense}")
        break

# Result
# print(result)