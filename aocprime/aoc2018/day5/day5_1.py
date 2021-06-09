#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=5)
puzzle_input = puzzle.get_input()

polymer = list(puzzle_input)

# Actual Code
idx = 0
original_len = len(polymer)
while idx < len(polymer) - 1:
  if polymer[idx] != polymer[idx + 1]:
    if polymer[idx].upper() ==  polymer[idx + 1].upper():
      del polymer[idx:idx+2]
      if idx > 0:
        idx -= 1
      idx -= 1
  idx += 1
  print("PROGRESS, current:", idx, "original_len:", original_len, end="\r")

# Result Parsing
print()
print(len(polymer))