#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=8)
puzzle_input = puzzle.get_input()

tree_info = list(map(int, puzzle_input.split(" ")))

def read_nodes(data):
    num_children, num_metadata = (data.pop(0), data.pop(0))
    for i in range(num_children):
        for md in read_nodes(data):
            yield md
    for i in range(num_metadata):
        yield data.pop(0)

print(sum(read_nodes(tree_info)))