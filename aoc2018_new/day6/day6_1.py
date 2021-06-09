#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from string import digits, ascii_letters
graph_map = digits + ascii_letters
# Input Parse
puzzle = AdventOfCode(year=2018, day=6)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "1, 1",
#     "1, 6",
#     "8, 3",
#     "3, 4",
#     "5, 5",
#     "8, 9"
# ]

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
areas = list(map(lambda x: 0, locations))

max_x = max(map(lambda loc: loc[0], locations)) + 1
max_y = max(map(lambda loc: loc[1], locations)) + 1

graph = [[None]*max_x for _ in range(max_y)]
def add_to_graph(point, loc):
    val = ""
    if loc is None:
        val = "."
    elif point == locations[loc]: 
        val = "~"
    else:
        val = graph_map[loc]
    graph[point[1]][point[0]] =  val

def display_graph():
    for row in graph:
        print("".join(row))
# Actual Code
for y in range(max_y):
    for x in range(max_x):
        current_location = (x, y)
        min_location, min_distance = (None, None)
        for idx, location in enumerate(locations):
            curr_location, curr_distance = (idx, manhattan_distance(current_location, location))
            if min_distance == None or curr_distance < min_distance:
                min_location, min_distance = curr_location, curr_distance
            elif min_distance == curr_distance:
                min_location = None
        # add_to_graph(current_location, min_location)
        if min_location is not None:
            if is_edge(current_location, (max_x-1, max_y-1)):
                # print(min_location, locations[min_location], "=>", current_location)
                areas[min_location] = float('inf')
            areas[min_location] += 1
# Result
# print(graph_map)
# display_graph()
print(max(filter(lambda a: a != float('inf'), areas)))