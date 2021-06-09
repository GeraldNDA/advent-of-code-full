#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=7)
puzzle_input = puzzle.get_input()

# Actual Code
result = puzzle_input

# Result
print(result)