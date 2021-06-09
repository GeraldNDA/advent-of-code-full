#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from collections import defaultdict

# Input Parse
puzzle = AdventOfCode(year=2018, day=17)
puzzle_input = puzzle.get_input()
# puzzle_input = [
# "x=495, y=2..7",
# "y=7, x=495..501",
# "x=501, y=3..7",
# "x=498, y=2..4",
# "x=506, y=1..2",
# "x=498, y=10..13",
# "x=504, y=10..13",
# "y=13, x=498..504",
# ]
spring_pos = (500, 0)
grid = defaultdict(lambda: None)
min_y = float('inf')
max_y = 0

def print_grid():
    min_x = min(grid, key=lambda p: p[0])[0]
    max_x = max(grid, key=lambda p: p[0])[0]
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if grid[(x, y)] is None:
                print(".", end="")
            elif grid[(x,y)] is RestingWater:
                print("~", end="")
            elif grid[(x,y)] is Spring:
                print("+", end="")
            elif grid[(x,y)] is FallingWater:
                print("|", end="")
            elif grid[(x,y)] is Clay:
                print("#", end="")
        print()

class Spring:
    pass

class Clay:
    pass

class Water:
    pass

class FallingWater(Water):
    pass

class RestingWater(Water):
    pass

BLOCKING_TYPE = {Clay, RestingWater}
WATER_TYPE = {FallingWater, RestingWater}

def parse_scan(scan_line):
    global grid, min_y, max_y
    scan_parts = scan_line.split(", ")
    scan_parts = dict(
        map(lambda p: p.split("="), scan_parts)
    )
    for coord_part, value in scan_parts.items():
        if '..' in value:
            value = tuple(map(int, value.split('..')))
        else:
            value = (int(value),)*2
        scan_parts[coord_part] = (value[0], value[1] + 1)
    for x in range(*scan_parts['x']):
        for y in range(*scan_parts['y']):
            grid[(x, y)] = Clay
            min_y = min(min_y, y)
            max_y = max(max_y, y)

for scan_line in puzzle_input:
    parse_scan(scan_line)

def above(coord):
    return (coord[0], coord[1]-1)
def below(coord):
    return (coord[0], coord[1]+1)
def beside_left(coord):
    return (coord[0]-1, coord[1])
def beside_right(coord):
    return (coord[0]+1, coord[1])

def find_clay_bounds(coord):
    assert(grid[below(coord)] in BLOCKING_TYPE)
    
    left_bound = beside_left(coord)
    right_bound = beside_right(coord)
    
    while grid[below(left_bound)] in BLOCKING_TYPE and grid[left_bound] is not Clay:
        left_bound = beside_left(left_bound)
    while grid[below(right_bound)] in BLOCKING_TYPE and grid[right_bound] is not Clay:
        right_bound = beside_right(right_bound)
    
    bounds_are_clay = grid[left_bound] == grid[right_bound] == Clay
    return left_bound, right_bound, bounds_are_clay

# Actual Code
grid[spring_pos] = Spring
grid[below(spring_pos)] = FallingWater
cursors = [below(spring_pos)]
while cursors:
    cursor = cursors.pop(0)
    if cursor[1] >= max_y:
        continue
    try:
        assert(grid[cursor] is FallingWater)
    except:
        print(cursor, grid[cursor], cursors)
        break
    
    if grid[below(cursor)] is None:
        grid[below(cursor)] = FallingWater
        cursors.append(below(cursor))
        continue

    if grid[below(cursor)] in BLOCKING_TYPE:
        leftmost, rightmost, bounds_are_clay = find_clay_bounds(cursor)
        fill_type = RestingWater if bounds_are_clay else FallingWater
        
        left_bound = leftmost[0]
        right_bound = rightmost[0]
        if grid[leftmost] is not None:
            left_bound += 1
        if grid[rightmost] is None:
            right_bound += 1
        # print(bounds_are_clay, leftmost, rightmost, grid[leftmost], grid[rightmost])
        for x in range(left_bound, right_bound):
            grid[(x, cursor[1])] = fill_type
            if (x, cursor[1]) in cursors:
                del cursors[cursors.index((x, cursor[1]))]
        if grid[below(leftmost)] is None:
            assert(fill_type is FallingWater)
            cursors.append(leftmost)
        if grid[below(rightmost)] is None:
            assert(fill_type is FallingWater)
            cursors.append(rightmost)
        
        if bounds_are_clay:
            for x in range(left_bound, right_bound):
                if grid[(x, cursor[1] - 1)] is FallingWater:
                    cursors.append((x, cursor[1] - 1))
        continue

# Result
water_count = 0
for coord, item in grid.items():
    _, y = coord
    if item is RestingWater:
        if min_y <= y <= max_y:
            water_count += 1
print(water_count)
