#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=22)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "depth: 510",
#     "target: 10,10"
# ]


def parse_input(inpt):
    depth = 0
    target = (0, 0)
    for line in inpt:
        line = line.split(" ")
        line[0] = line[0].strip(":")
        if line[0] == "depth":
            depth = int(line[1])
        if line[0] == "target":
            target = tuple(map(int, line[1].split(",")))
    return depth, target

depth, target = parse_input(puzzle_input)

erosion_level_map = {}
geographical_index_map = {}
# Actual Code
result = puzzle_input
def erosion_level(coords):
    if coords not in erosion_level_map:
        erosion_level_map[coords] = (
            geographical_index(coords) + depth
        ) % 20183;
    return erosion_level_map[coords]

def geographical_index(coords):
    global target
    if coords not in geographical_index_map:
        x,y = coords
        if coords in {(0,0), target}:
            geographical_index_map[coords] = 0
        elif x == 0:
            geographical_index_map[coords] = y * 48271
        elif y == 0:
            geographical_index_map[coords] = x * 16807
        else:
            geographical_index_map[coords] = erosion_level((x-1, y)) * erosion_level((x, y-1))
    return geographical_index_map[coords]

risk_level = 0
for x in range(target[0] + 1):
    for y in range(target[1] + 1):
        risk_level += erosion_level((x, y)) % 3

# Result
print(risk_level)