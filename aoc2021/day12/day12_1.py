#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from collections import defaultdict

# Input Parse
puzzle = AdventOfCode(year=2021, day=12)
puzzle_input = puzzle.get_input()

cave_connections = defaultdict(list)
for connection in puzzle_input:
    start, end = connection.split("-")
    cave_connections[start].append(end)
    if start != "start" and end != "end":
        cave_connections[end].append(start)

# Actual Code
paths = [("start",)]
complete_paths = []
while paths:
    path = paths.pop()
    last_cave = path[-1]
    for next_cave in cave_connections[last_cave]:
        if next_cave.islower() and next_cave in path:
            continue
        next_path = path + (next_cave,)
        if next_cave == "end":
            complete_paths.append(next_path)
        else:
            paths.append(next_path)

# Result
print(len(complete_paths))