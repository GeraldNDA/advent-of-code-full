#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=11)
puzzle_input = puzzle.get_input()
serial_input = int(puzzle_input)

# Actual Code
grid  = {}

for y in range(1, 300 + 1):
    for x in range(1, 300 + 1):
        coord = (x, y)
        rack_id = x + 10
        power_level = rack_id * y + serial_input
        power_level *= rack_id
        power_level = ( power_level // 100) % 10 # Get 3rd digit7
        power_level -= 5
        grid[coord] = power_level
coords = []
for x in range(1, 300 + 1 - 3):
    for y in range(1, 300 + 1 - 3):
        coords.append((x, y))

def power_area(coord):
    return sum(
        sum(grid[(coord[0] + c, coord[1] + r)] for r in range(3))
        for c in range(3)
    )
# Result
best_coords = max(coords, key=power_area)
print(best_coords, power_area(best_coords))
for y in range(best_coords[1], best_coords[1] + 3):
    for x in range(best_coords[0], best_coords[0] + 3):
        print(grid[(x, y)], end= " ")
    print()