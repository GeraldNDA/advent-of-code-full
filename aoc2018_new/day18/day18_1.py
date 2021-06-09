#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=18)
puzzle_input = puzzle.get_input()
MINUTES_TO_TEST = 10
lumber_collection_area = list(map(list, puzzle_input))
area_size = (len(lumber_collection_area), len(lumber_collection_area[0]))
def get_neighbours(pos):
    r, c = pos
    if r > 0:
        yield (r - 1, c)
        if c  > 0:
            yield (r - 1, c - 1)
        if c < area_size[1] - 1:
            yield (r - 1, c + 1)

    if r < area_size[0] - 1:
        yield (r + 1, c)
        if c  > 0:
            yield (r + 1, c - 1)

        if c < area_size[1] - 1:
            yield (r + 1, c + 1)
    if c  > 0:
        yield (r, c - 1)

    if c < area_size[1] - 1:
        yield (r, c + 1)
            
def pos_to_values(poses):
    for r, c in poses:
        yield lumber_collection_area[r][c]

def gen_poses(r_max, c_max):
    for r in range(r_max):
        for c in range(c_max):
            yield (r, c)

def is_open_acre(contents):
    return contents == "."
def is_tree_filled(contents):
    return contents == "|"
def is_lumberyard(contents):
    return contents == "#"

def update_collection_area():
    global lumber_collection_area
    duplicate_area = list(map(list, lumber_collection_area))
    for pos in gen_poses(*area_size):
        r,c = pos
        neighbours = "".join(pos_to_values(get_neighbours(pos)))
        if is_open_acre(lumber_collection_area[r][c]):
            if neighbours.count("|") >= 3:
                duplicate_area[r][c] = "|"
        if is_tree_filled(lumber_collection_area[r][c]):
            if neighbours.count("#") >= 3:
                duplicate_area[r][c] = "#"
        if is_lumberyard(lumber_collection_area[r][c]):
            is_still_lumberyard = neighbours.count("#") >= 1 and neighbours.count("|") >= 1
            if not is_still_lumberyard:
                duplicate_area[r][c] = "."
    lumber_collection_area = duplicate_area
    
# Actual Code
tracker = []
current_area = None
last_minute = 0
for _ in range(MINUTES_TO_TEST):
    last_minute = _ + 1
    update_collection_area()
    current_area = "".join("".join(r) for r in lumber_collection_area)
    if current_area in tracker:
        break
    else:
        tracker.append(current_area)

wooded_acre_count = 0
lumberyard_count = 0


last_found = tracker.index(current_area) + 1
print(last_found)
print(last_minute)
pattern = tracker[last_found - 1:]
minutes_left = MINUTES_TO_TEST - last_minute
pattern_index = minutes_left % len(pattern)
last_yard = pattern[pattern_index]

for idx in range(len(pattern)):
    idx = (idx + 1) % len(pattern)
    update_collection_area()
    assert(pattern[idx] == "".join("".join(r) for r in lumber_collection_area)), idx

wooded_acre_count = last_yard.count("|")
lumberyard_count = last_yard.count("#")


# Result
print(wooded_acre_count * lumberyard_count)