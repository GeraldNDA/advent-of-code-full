#!/usr/bin/env python3
# Imports
import re

from math import floor, copysign
from aoc import AdventOfCode
from itertools import combinations
from collections import defaultdict
from statistics import median

sign = lambda x: copysign(1, x)
# Input Parse
puzzle = AdventOfCode(year=2018, day=23)
puzzle_input = puzzle.get_input()
puzzle_input = [
    "pos=<10,12,12>, r=2",
    "pos=<12,14,12>, r=2",
    "pos=<16,12,12>, r=4",
    "pos=<14,14,14>, r=6",
    "pos=<50,50,50>, r=200",
    "pos=<10,10,10>, r=5",
]


class Nanobot:
    NANOBOT_INFO_LINE_MATCHER = re.compile(r"pos=<\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*>, r=\s*(-?\d+)\s*")
    
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    
    def distance(self, other):
        if type(other) is Nanobot:
            other_pos = other.pos
        elif type(other) is tuple and len(other) == 3:
            other_pos = other
        else:
            raise ValueError(other)
        return sum(abs(self.pos[i] - other_pos[i]) for i in range(3))

    def in_range(self, other):
        return self.distance(other) <= self.radius

    def __gt__(self, other):
        if type(other) is Nanobot:
            return self.radius > other.radius
        raise NotImplementedError
    def __repr__(self):
        return f"Nanobot(pos=<{self.pos[0]},{self.pos[1]},{self.pos[2]}>, r={self.radius})"
    
    def bots_in_range(self, bots):
        bots_in_range = 0
        for bot in bots:
            if self.in_range(bot):
                bots_in_range += 1
        return bots_in_range
    
        

    @staticmethod
    def parse(line):
        bot_info = Nanobot.NANOBOT_INFO_LINE_MATCHER.match(line)
        if not bot_info:
            raise ValueError(line)
        else:
            bot_info = bot_info.groups()
            return Nanobot(tuple(map(int, bot_info[0:3])), int(bot_info[3]))

# Actual Code
def pos_range(lower_bound, upper_bound):
    for x in range(lower_bound[0], upper_bound[0]):
        for y in range(lower_bound[1], upper_bound[1]):
            for z in range(lower_bound[2], upper_bound[2]):
                yield (x, y, z)

def distance_from_start(pos):
    return sum(map(abs, pos))

def median_pos(bots):
    return tuple(
        median(bot.pos[i] for bot in bots)
        for i in range(3)
    )

def have_overlap(bot1, bot2):
    if bot2.in_range(bot1) or bot1.in_range(bot2):
        return True
    distance_vector = tuple(bot1.pos[i] - bot2.pos[i] for i in range(3))
    distance = sum(distance_vector[i]**2 for i in range(3)) ** 0.5
    unit_distance_vector = tuple(displacement/distance for displacement in distance_vector)
    radius_edge = tuple(
        floor(bot1.pos[i] + unit_distance_vector[i]*bot1.radius)
        for i in range(3)
    )
    return bot2.in_range(radius_edge)

bots = tuple(map(Nanobot.parse, puzzle_input))
overlap_counts = defaultdict(set)
for (idx1, bot1), (idx2, bot2) in combinations(enumerate(bots), 2):
    overlap = have_overlap(bot1, bot2)
    overlap_counts[bot1].add(idx2)
    overlap_counts[bot2].add(idx1)
most_overlap = max(overlap_counts.values(), key=len)
bot_list = tuple(map(lambda i: bots[i], most_overlap))
print(bot_list)
start_pos = median_pos(bot_list)
dirs = {
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (-1,0,0),
    (0,-1,0),
    (0,0,-1),
}
def add_dir(pos, direction):
    return tuple(pos[i] + direction[i] for i in range(3))
original_dist = sum(
    int(bot.in_range(start_pos))
    for bot in bots
)
curr_pos = start_pos
print("START:", start_pos)
print("START_DIST:", original_dist)
print("BOT_DIST:", len(bot_list))
for i in range(3):
    done = False
    while not done:
        print(curr_pos, end="\r")
        from_start = int(sign(0 - curr_pos[i]))
        new_pos = tuple(
            curr_pos[p_idx] + int(p_idx == i)*from_start
            for p_idx in range(3)
        )
        new_dist = sum(
            int(bot.in_range(curr_pos))
            for bot in bots
        )
        if new_dist < original_dist:
            break
        else:
            curr_pos = new_pos
# lower_bound_pos = tuple(min(map(lambda b: b.pos[i], bots)) for i in range(3))
# upper_bound_pos = tuple(max(map(lambda b: b.pos[i], bots)) for i in range(3))
# print(lower_bound_pos, upper_bound_pos)
# has_most_in_range = None
# num_in_range = 0
# for pos in pos_range(lower_bound_pos, upper_bound_pos):
#     in_range_of_count = sum(int(bot.in_range(pos)) for bot in bots)
#     if in_range_of_count > num_in_range:
#         has_most_in_range = pos
#         num_in_range = in_range_of_count
#     elif in_range_of_count == num_in_range and num_in_range > 0:
#         has_most_in_range = min(pos, has_most_in_range, key=distance_from_start)
# Result
# print(distance_from_start(has_most_in_range))