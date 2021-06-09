#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=20)
puzzle_input = puzzle.get_input()

# Actual Code
path_regex = puzzle_input

def get_closing_bracket(path_regex, idx):
    assert(path_regex[idx] == "(")
    bracket_stack = 0
    while idx < len(path_regex):
        idx += 1
        if path_regex[idx] == "(":
            bracket_stack += 1
        if path_regex[idx] == ")":
            if bracket_stack == 0:
                return idx
            bracket_stack -= 1
    return None

def get_longest(path_regex, start_index, end_index):
    path = [""]
    idx = start_index
    while idx < end_index + 1:
        item = path_regex[idx]

        if item in "NESW":
            path[-1] += item
        elif item == "|":
            path.append("")
        elif item == "(":
            end_idx = get_closing_bracket(path_regex, idx)
            path[-1] += get_longest(path_regex, idx + 1, end_idx - 1)
            idx = end_idx
        idx += 1
    if "" in path:
        return ""
    else:
        return max(path, key=len)

far_room_path = get_longest(path_regex, 1, len(path_regex) - 2)
# Result
print(far_room_path, len(far_room_path))