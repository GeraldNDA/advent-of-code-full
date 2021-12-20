#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
from typing import List, NamedTuple, Tuple
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
    if end != "start":
        cave_connections[start].append(end)
    if start != "start":
        cave_connections[end].append(start)

# Actual Code
class Path(NamedTuple):
    path: Tuple[str]
    double_visit: bool = False

    def can_visit(self, cave):
        return not (cave.islower() and self.double_visit and self.path.count(cave) > 0)

    def visit(self, cave):
        return Path(path=(*self.path, cave), double_visit=self.double_visit or (cave.islower() and cave in self.path))

    def last_cave(self):
        return self.path[-1]

paths = [Path(path=("start",))]
complete_paths = []
while paths:
    path = paths.pop()
    for next_cave in cave_connections[path.last_cave()]:
        if not path.can_visit(next_cave):
            continue
        next_path = path.visit(next_cave)
        if next_cave == "end":
            complete_paths.append(next_path)
        else:
            paths.append(next_path)

# Result
print(len(complete_paths))