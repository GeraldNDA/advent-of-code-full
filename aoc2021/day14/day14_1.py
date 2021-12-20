#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller

# Input Parse
puzzle = AdventOfCode(year=2021, day=14)
puzzle_input = puzzle.get_input()


puzzle_input = iter(puzzle_input)
polymer_template = next(puzzle_input)
next(puzzle_input) # blank_Line

insertion_rule = {pair: to_insert for pair, to_insert in map(methodcaller("split", " -> "), puzzle_input)}

# Actual Code
new_template = [polymer_template[0]]
for _ in range(2):
    for pair in zip(polymer_template[:-1], polymer_template[1:]):
        new_template.extend((insertion_rule["".join(pair)], pair[-1]))
    polymer_template = "".join(new_template)
    new_template = [polymer_template[0]]

elements = set(polymer_template)
element_counts = {element: polymer_template.count(element) for element in elements}
# Result
print(max(element_counts.values()) - min(element_counts.values()))