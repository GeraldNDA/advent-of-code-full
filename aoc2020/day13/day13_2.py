#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=13)
puzzle_input = puzzle.get_input()

depart_time = int(puzzle_input[0])
busses = tuple(map(lambda bus_id: int(bus_id) if bus_id != "x" else None, puzzle_input[1].split(",")))

# Actual Code
next_bus = min(filter(None, busses), key=lambda bus_id: bus_id - (depart_time % bus_id))

# Result
print(next_bus*(next_bus - (depart_time % next_bus)))