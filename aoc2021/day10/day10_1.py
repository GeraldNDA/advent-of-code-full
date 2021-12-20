#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=10)
puzzle_input = puzzle.get_input()

subsystem_syntax = puzzle_input


chunk_info = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
scoring = dict([
    (")", 3),
    ("]", 57),
    ("}", 1197),
    (">", 25137),
])
# Actual Code
illegal_points = 0
for line in subsystem_syntax:
    stack = []
    for char in line:
        if char in chunk_info:
            stack.append(chunk_info[char])
        elif char == stack[-1]:
            stack.pop()
        else:
            illegal_points += scoring[char]
            break


# Result
print(illegal_points)