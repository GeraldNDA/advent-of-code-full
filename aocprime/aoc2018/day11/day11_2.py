#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from functools import partial

# Input Parse
puzzle = AdventOfCode(year=2018, day=11)
puzzle_input = puzzle.get_input()
serial_input = int(puzzle_input)
GRID_SIZE = 300

# Actual Code
grid  = {}

for y in range(1, GRID_SIZE + 1):
    for x in range(1, GRID_SIZE + 1):
        coord = (x, y)
        rack_id = x + 10
        power_level = rack_id * y + serial_input
        power_level *= rack_id
        power_level = ( power_level // 100) % 10 # Get 3rd digit7
        power_level -= 5
        grid[coord] = power_level


def gen_coords(lower, top):
    for x in range(lower[0], top[0] + 1):
        for y in range(lower[1], top[1] + 1):
            yield (x, y)

area_map = {}
def power_area(start, size):
    if (start, size) in area_map:
        return area_map[(start, size)]
    if size == 1:
        return grid[start]
    splits = set()
    sub_size = size // 2
    splits.add((start, sub_size))
    splits.add(((start[0], start[1] + sub_size), sub_size))
    splits.add(((start[0] + sub_size, start[1]), sub_size))
    splits.add(((start[0] + sub_size, start[1] + sub_size), sub_size))
    area_map[(start, size)] = 0
    if size % 2:
        bottom_corner = (start[0] + size - 1, start[1] + size - 1)
        area_map[(start, size)] += sum(grid[(bottom_corner[0], start[1] + amount)] for amount in range(size))
        area_map[(start, size)] += sum(grid[(start[0] + amount, bottom_corner[1])] for amount in range(size))
        area_map[(start, size)] -= grid[bottom_corner]
    for split in splits:
        area_map[(start, size)] += power_area(*split)
    return area_map[(start, size)]

def left_over(start, parent_size, offset):
    curr_total = 0
    corner = (
        start[0] + (parent_size - 1)*int(not offset[0]),
        start[1] + (parent_size - 1)*int(not offset[1])
    )
    curr_total -= grid[corner]
    # get top or bottom
    curr_total += sum(
        grid[(start[0] + amount, corner[1])] 
        for amount in range(parent_size)
    )
    # get left or right
    curr_total += sum(
        grid[(corner[0], start[1] + amount)] 
        for amount in range(parent_size)
    )
    return curr_total
# Result
max_start, max_size = None, None
max_area = None
for size in reversed(range(1, 300+1)):
    last_coord = 300 - size + 1
    print(size, end="\r")
    for x in range(1, last_coord + 1):
        for y in range(1, last_coord + 1):
            curr_area = power_area((x, y), size)
            if max_area is None or curr_area > max_area:
                max_start = (x, y)
                max_size = size
                max_area = curr_area
print()
print(max_start, max_size)
# 232,251,12
