#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from collections import defaultdict
# Input Parse
puzzle = AdventOfCode(year=2020, day=10)
puzzle_input = puzzle.get_input()
jolt_adapters = [0] + list(sorted(map(int, puzzle_input)))
jolt_adapters.append(3 + max(jolt_adapters))

# Actual Code
jolt_differences = defaultdict(int)
for from_adapter, to_adapter in zip(jolt_adapters[:-1], jolt_adapters[1:]):
    jolt_differences[to_adapter - from_adapter] += 1

print(jolt_differences)
# Result
print(jolt_differences[1]*jolt_differences[3])