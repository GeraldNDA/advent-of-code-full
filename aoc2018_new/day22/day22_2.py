#!/usr/bin/env python3
# Imports
from enum import Enum
from collections import defaultdict

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

depth, target_pos = parse_input(puzzle_input)

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
    if coords not in geographical_index_map:
        x,y = coords
        if coords in {(0,0), target_pos}:
            geographical_index_map[coords] = 0
        elif x == 0:
            geographical_index_map[coords] = y * 48271
        elif y == 0:
            geographical_index_map[coords] = x * 16807
        else:
            geographical_index_map[coords] = erosion_level((x-1, y)) * erosion_level((x, y-1))
    return geographical_index_map[coords]

class Region(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

    def allowed_tools(self):
        return set(tool for tool in Tool if tool.value != self.value)
    
    @classmethod
    def get_region(cls, coords):
        assert all(coord >=0 for coord in coords)
        try:
            return cls(erosion_level(coords) % 3)
        except:
            raise ValueError(f"Died with coords {coords}")
            # raise

class Tool(Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2

    def allowed_regions(self):
        return set(region for region in Region if region.value != self.value)

class PosInfo(object):
    DIRS = (
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    )
    CHANGE_TIME = 7
    MOVE_TIME = 1

    def __init__(self, pos, tool, time=0):
        self.pos = pos
        self.tool = tool
        self.time = time
    
    def next_points(self):
        curr_region = Region.get_region(self.pos)
        curr_allowed_tools = Region.allowed_tools(curr_region) - {self.tool,}
        # Move closer
        for dir in PosInfo.DIRS:
            new_pos = tuple(sum(p) for p in zip(dir, self.pos))
            if any(p < 0 for p in new_pos):
                continue
            new_region = Region.get_region(new_pos)
            allowed_tools = Region.allowed_tools(new_region)
            if self.tool in allowed_tools:
                yield PosInfo(new_pos, self.tool, self.time+PosInfo.MOVE_TIME)
        # Change equipment
        for tool in curr_allowed_tools:
            yield PosInfo(self.pos, tool, self.time+PosInfo.CHANGE_TIME)
    
    def min_distance(self, target):
        manhattan_dist = sum([abs(p - t) for p, t in zip(self.pos, target.pos)])
        change_time = 0 if target.tool is self.tool else 7
        return manhattan_dist + change_time
    
    def min_time(self, target):
        return self.min_distance(target) + self.time
    
    def __eq__(self, other):
        return self.pos == other.pos and self.tool is other.tool
    
    def __repr__(self):
        return f"{type(self).__name__}(pos={self.pos}, tool={self.tool}, time={self.time})"
    
    def to_tuple(self):
        return self.pos, self.tool

wavefront = [PosInfo((0, 0), Tool.TORCH)]
target = PosInfo(target_pos, Tool.TORCH)
known_dist = defaultdict(lambda: float("inf"))
min_dist = wavefront[0].min_distance(target)
# WAYYYYYYYYYY TOO SLOW (but this is A* :O)
while wavefront:
    curr_pos = wavefront.pop(0)
    min_dist = min(min_dist, curr_pos.min_distance(target))
    if curr_pos == target:
        print()
        print(curr_pos)
        break
    
    for pos in curr_pos.next_points():
        if known_dist[pos.to_tuple()] > pos.time:
            wavefront.append(pos)
            known_dist[pos.to_tuple()] = pos.time
    wavefront.sort(key=lambda p: p.min_time(target))
    print(f"len(wavefront)={len(wavefront)}, dist={wavefront[0].min_distance(target)}, min_dist={min_dist}" + " "*50, end="\r")


