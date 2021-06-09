#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=20)
puzzle_input = puzzle.get_input()

# Actual Code
path_regex = puzzle_input
threshold = 1000

# path_regex = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
# threshold = 19

#initial attempt
"""
def get_path_lengths(path_regex, start_index, threshold):
    path_lengths = []
    curr_threshold = threshold
    idx = start_index
    over_count = 0
    item = path_regex[idx]
    done = False
    while not done:
        if item in "NESW":
            curr_threshold -= 1
            if curr_threshold <= 0:
                over_count += 1
        elif item == "|":
            path_lengths.append(threshold - curr_threshold)
            curr_threshold = threshold
        elif item == "(":
            sub_over_count, min_sub_path_length, idx =  get_path_lengths(path_regex, idx + 1, curr_threshold)
            over_count += sub_over_count
            curr_threshold -= min_sub_path_length
        elif item == "$" or item == ")":
            path_lengths.append(threshold - curr_threshold)
            done = True
        if not done:
            idx += 1
            item = path_regex[idx]
    if min(path_lengths) == 0:
        for pl in path_lengths:
            if threshold <= 0:
                pass
            elif threshold <= pl:
                over_count -= (pl - threshold + 1)
                if threshold <= pl//2:
                    over_count += pl//2 - threshold +1
    return over_count, min(path_lengths), idx
"""

MOVE = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}

def get_visited_rooms(path_regex, start_index, rooms, start_room=(0,0), start_pl=0):
    path_lengths = []
    curr_room = start_room
    curr_pl = start_pl
    idx = start_index
    item = path_regex[idx]
    done = False
    while not done:
        # print(curr_pl, curr_room)
        if item in "NESW":
            curr_pl += 1
            curr_room = tuple( curr_room[i] + MOVE[item][i] for i in range(2) )
            if curr_room not in rooms:
                rooms[curr_room] = curr_pl
        elif item == "|":
            path_lengths.append(curr_pl)
            curr_room = start_room
            curr_pl = start_pl
        elif item == "(":
            curr_pl, idx =  get_visited_rooms(path_regex, idx + 1, rooms, curr_room, curr_pl)
            # curr_pl = min_sub_path_length
        elif item == "$" or item == ")":
            path_lengths.append(curr_pl)
            done = True
        if not done:
            idx += 1
            item = path_regex[idx]
    return min(path_lengths), idx
    


rooms = {}
_, _ = get_visited_rooms(path_regex, 1, rooms, start_room=(0,0), start_pl=0)
over_count = len(list(filter(lambda r: rooms[r] >= threshold, rooms.keys())))
# Result
print(over_count)
# print(list(filter(lambda r: r[1] >= threshold, rooms.items())))