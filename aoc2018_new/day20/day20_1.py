#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=20)
puzzle_input = puzzle.get_input()

# Actual Code
path_regex = puzzle_input

def get_longest(path_regex, start_index):
    path = [""]
    idx = start_index
    item = path_regex[idx]
    done = False
    while not done:
        if item in "NESW":
            path[-1] += item
        elif item == "|":
            path.append("")
        elif item == "(":
            max_sub, idx =  get_longest(path_regex, idx + 1)
            path[-1] += max_sub
        elif item == "$" or item == ")":
            done = True
        if not done:
            idx += 1
            item = path_regex[idx]
    if "" in path:
        return ("", idx)
    else:
        return (max(path, key=len), idx)

far_room_path, _ = get_longest(path_regex, 1)
# Result
print(len(far_room_path))