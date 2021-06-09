#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from collections import defaultdict, OrderedDict

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
        ) % 20183
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

class Torch:
    pass
class ClimbingGear:
    pass

dirs = {(1, 0), (0, 1), (-1, 0), (0, -1)}
start = ((0, 0), Torch)
first = (0, None)
horizon = OrderedDict([ (start, first )])
equipment_options = [
    {ClimbingGear, Torch},
    {ClimbingGear, None},
    {Torch, None}
]
# Prep erosion level map
for x in range(target[0] + 100):
    for y in range(target[1] + 100):
        erosion_level((x, y))

# def target_is_done():
#     if (target, Torch) in overall_map:
#         print(f"FOUND TARGET! {len(horizon)}", end="\r")
#         return not any(
#             (
#                 (target[0] + direction[0], target[1] + direction[1]),
#                 equip
#             ) in horizon
#             for direction in dirs for equip in {ClimbingGear, Torch, None}
#         )
#     return False

def distance_from_target(pos):
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1])


seen = dict()
done = False
while not done:
    (curr, curr_equipment), (time, pre) = horizon.popitem(last=False)
    # print(len(horizon),distance_from_target(curr), " "*20, end="\r")
    if curr == target and curr_equipment == Torch:
        done = True
        
        seen[(curr,curr_equipment)] = (time, pre)
        print()
        print("="*30)
        # for item in horizon:
        #     print(item, horizon[item], distance_from_target(item[0]))
        print(time)
        break
    seen[(curr,curr_equipment)] = (time, pre)
    for direction in dirs:
        new_pos = (
            curr[0] + direction[0],
            curr[1] + direction[1]
        )
        if new_pos[0] >= 0 and new_pos[1] >= 0:
            region_type = erosion_level(new_pos) % 3
            equip_options = equipment_options[region_type] & equipment_options[erosion_level(curr) % 3] 
            if new_pos == target:
                equip_options == {Torch,}
            for opt in equipment_options[region_type]:
                change_time = 0 if opt is curr_equipment else 7
                new_time = min( time + 1 + change_time , seen.get((new_pos, opt), (float("inf"), None))[0] )
                if (new_pos, opt) not in seen or new_time < seen[(new_pos, opt)][0]:
                    if (new_pos, opt) not in horizon or new_time < horizon[(new_pos, opt)][0]:
                        horizon[(new_pos, opt)] = (new_time, (curr, curr_equipment))

            # if curr_equipment not in equip_options:
            #     for opt in equipment_options[region_type]:
            #         new_time = min( time + 8 , seen.get((new_pos, opt), (float("inf"), None))[0] )
            #         if (new_pos, opt) not in seen or new_time < seen[(new_pos, opt)][0]:
            #             horizon[(new_pos, opt)] = (new_time, (curr, curr_equipment))
            # else:
            #     new_time = min( time + 1 ,seen.get((new_pos, curr_equipment), (float("inf"), None))[0] )
            #     if (new_pos, curr_equipment) not in seen or new_time < seen[(new_pos, curr_equipment)][0]:
            #         horizon[(new_pos, curr_equipment)] = (new_time, (curr, curr_equipment))
    horizon = OrderedDict(sorted( horizon.items(), key=lambda p: p[1][0] + distance_from_target(p[0][0]) ) )

def reconstruct_path():
    curr = (target, Torch)
    path = []
    while curr != ((0,0), Torch):
        path.append((curr, seen[curr][0]))
        curr = seen[curr][-1]
    return list(reversed(path + [(((0,0), Torch), 0)]))
# path = reconstruct_path()
# for item in path:
#     print(item)
# print(len(path))
# for item in horizon:
#     print(item[0], horizon[item][0], distance_from_target(item[0]))


# print()
# print("="*30)
# print(horizon[(target, Torch)])


# # while (target, Torch) not in overall_map:
# while not target_is_done():
#     len_horizon = len(horizon)
#     print(len_horizon, end="\r")
#     for _ in range(len_horizon):
#         # print(len(horizon), end="\r")
#         curr, curr_equipment = horizon.pop(0)
#         for direction in dirs:
#             new_pos = (
#                 curr[0] + direction[0],
#                 curr[1] + direction[1]
#             )
#             # print(new_pos)
#             if new_pos[0] >= 0 and new_pos[1] >= 0:
#                 # print("C", new_pos)
#                 try:
#                     region_type = erosion_level(new_pos) % 3
#                 except Exception:
#                     raise ValueError(new_pos)
#                 new_map_info = {}
#                 if curr_equipment not in equipment_options[region_type] or new_pos == target:
#                     for equipment_option in equipment_options[region_type]:
#                         to_add = 7 if equipment_option != curr_equipment else 1
#                         new_map_info[(new_pos, equipment_option)] = min( 
#                             overall_map[
#                                 (curr, curr_equipment)
#                             ] + to_add,
#                             overall_map[(new_pos, equipment_option)]
#                         )
#                 else:
#                     new_map_info[(new_pos, curr_equipment)] = min(
#                         overall_map[
#                             (curr, curr_equipment)
#                         ] + 1,
#                         overall_map[(new_pos, curr_equipment)]
#                     )
                
#                 for pos_item in set(new_map_info.keys()):
#                     if overall_map[pos_item] == new_map_info[pos_item]:
#                         del new_map_info[pos_item]
#                 horizon.extend(set(new_map_info.keys()))
#                 # print(horizon)
#                 overall_map.update(new_map_info)

# # Result
# print("0"*30)
# print(overall_map[(target, Torch)])