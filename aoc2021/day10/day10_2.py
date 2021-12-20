#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from statistics import median

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
    (")", 1),
    ("]", 2),
    ("}", 3),
    (">", 4),
])
# Actual Code
scores = []
for line in subsystem_syntax:
    stack = []
    for char in line:
        if char in chunk_info:
            stack.append(chunk_info[char])
        elif char == stack[-1]:
            stack.pop()
        else:
            break
    else:
        score = 0
        for completed_char in reversed(stack):
            score *= 5
            score += scoring[completed_char]
        scores.append(score)



# Result
print(median(scores))