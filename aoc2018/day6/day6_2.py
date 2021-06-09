#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=6)
puzzle_input = puzzle.get_input()
puzzle_input = [
    "1, 1",
    "1, 6",
    "8, 3",
    "3, 4",
    "5, 5",
    "8, 9"
]
max_distance = 32
# max_distance = 10000

def input_to_coords(line):
    return tuple(map(int, line.split(",")))

def manhattan_distance(coord1, coord2):
    return sum(map(lambda idx: abs(coord1[idx] - coord2[idx]), range(2)))

def is_edge(coord, max_coord):
    if 0 in coord:
        return True
    if max_coord[0] == coord[0] or max_coord[1] == coord[1]:
        return True
    return False

locations = list(map(input_to_coords, puzzle_input))
len_locations = len(locations)


min_x = min(map(lambda loc: loc[0], locations))
min_y = min(map(lambda loc: loc[1], locations))
max_x = max(map(lambda loc: loc[0], locations))
max_y = max(map(lambda loc: loc[1], locations))
width = (max_x - min_x)
height = (max_y - min_y)
required_radius = (max_distance  - width - height) // len_locations

print(required_radius)
max_x += required_radius + 1
max_y += required_radius + 1
min_x -= required_radius
min_y -= required_radius

region_size = 0
# Actual Code
for y in range(min_y, max_y):
    for x in range(min_x, max_x):
        total_distance = 0
        idx = 0
        while total_distance < max_distance and idx < len_locations:
            total_distance += manhattan_distance((x, y), locations[idx])
            idx += 1
        if total_distance < max_distance:
            region_size += 1
# Result
print(region_size)