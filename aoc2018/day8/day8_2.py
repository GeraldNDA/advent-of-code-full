#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=8)
puzzle_input = puzzle.get_input()

tree_info = list(map(int, puzzle_input.split(" ")))

def get_value(data):
    num_children, num_metadata = (data.pop(0), data.pop(0))
    children_values = []
    for i in range(num_children):
        children_values.append(get_value(data))
    
    my_value = 0
    for i in range(num_metadata):
        metadata_value = data.pop(0)
        if not children_values:
            my_value += metadata_value
        elif (metadata_value-1) in range(num_children):
            my_value += children_values[metadata_value - 1]
    return my_value

print(get_value(tree_info))