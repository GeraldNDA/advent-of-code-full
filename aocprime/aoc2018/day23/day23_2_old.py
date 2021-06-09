#!/usr/bin/env python3
# Imports
import re
import sys

from math import floor, copysign, inf
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
    
    def overlaps(self, other_bot):
        return NanobotOverlap.have_overlap((self, other_bot))
    
    def overlapping_bots(self, bots):
        return tuple(self.overlaps(bot) for bot in bots)

    @staticmethod
    def parse(line):
        bot_info = Nanobot.NANOBOT_INFO_LINE_MATCHER.match(line)
        if not bot_info:
            raise ValueError(line)
        else:
            bot_info = bot_info.groups()
            return Nanobot(tuple(map(int, bot_info[0:3])), int(bot_info[3]))

class NanobotOverlap:
    def __init__(self, overlap=None):
        self.overlap = [(None,)*2]*3
        self.considered_bots = set()
        if overlap:
            self.overlap = list(overlap.overlap)
            self.considered_bots = set(overlap.considered_bots)

    def __add__(self, bot):
        """Immutable version of add()"""
        return NanobotOverlap(overlap=self).add(bot)

    def __radd__(self, bot):
        """Immutable version of add()"""
        return NanobotOverlap(overlap=self).add(bot)

    def add(self, bot):
        self.considered_bots.add(bot)
        for dim, overlap_range in enumerate(self.overlap):
            bot_range = (bot.pos[dim] - bot.radius, bot.pos[dim] + bot.radius)
            if overlap_range == (None, None):
                self.overlap[dim] = bot_range
                continue
            if overlap_range is None:
                continue
            if overlap_range[0] <= bot_range[0] <= overlap_range[1]:
                if overlap_range[0] <= bot_range[1] <= overlap_range[1]:
                    self.overlap[dim] = bot_range
                else:
                    self.overlap[dim] = (bot_range[0], overlap_range[1])
            elif overlap_range[0] <= bot_range[1] <= overlap_range[1]:
                self.overlap[dim] = (overlap_range[0], bot_range[1])
            elif bot_range[0] <= overlap_range[0] <= bot_range[1] and bot_range[0] <= overlap_range[1] <= bot_range[1]:
                # overlap range stays same
                pass
            else:
                self.overlap[dim] = None
        return self

    def __bool__(self):
        return all(self.overlap)
    
    def center(self):
        if self:
            return tuple((r[0] + r[1])//2 for r in self.overlap)
        return None
    
    @staticmethod
    def have_overlap(bots, overlap=None):
        overlap = overlap or sum(bots, NanobotOverlap())
        centre = overlap.center()
        if not centre:
            return False
        centres = [centre]
        for dim in range(3):
            dim_range = overlap.overlap[dim]
            if 0 < dim_range[1] - dim_range[0] <= 2:
                new_centre = list(centre)
                for val in range(dim_range[0], dim_range[1] + 1):
                    new_centre[dim] = val
                    centres.append(tuple(new_centre))
        return any(all(bot.in_range(centre) for bot in bots) for centre in centres)

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

def have_overlap(bot_list, debug=False):
    overlap_range = NanobotOverlap()
    for bot in bot_list:
        overlap_range.add(bot)
        
    # print(len(bot_list), bot_list, ">>", bool(overlap_range))
    return overlap_range

# def overlapping_groups(bot_list, group_size):
#     groups = []
#     for combo in combinations(bot_list, group_size):
#         overlap = have_overlap(combo)
#         if overlap:    
#             groups.append(combo)
#     return groups

# def get_potential_up_groups(group_list, num_bots):
#     grouped_bots = set()
#     for group in group_list:
#         grouped_bots |= set(group)
#     up_groups = list()
#     for group in group_list:
#         for bot in (grouped_bots - set(group)):
#             up_group = group + (bot,)
#             if up_group not in up_groups:
#                 for combo in combinations(up_group, num_bots):
#                     if combo not in group_list:
#                 else:
#                     up_groups.append(up_group)

#     return up_groups
bots = set(map(Nanobot.parse, puzzle_input))
curr_max_groups = set()
seen = set()
max_group_len = 0
# Sort groups before adding to known_groups
# Add a seen set so bad paths aren't explored
# Only keep max length group (if current group is longer than rest, then throw out the rest)
flat_count = 0
overlaps_bots = {b:set(filter(b.overlaps,bots)) - set([b]) for b in bots}
overlap_sort = lambda b: len(overlaps_bots[b]) 
def build_bot_groups(bots, curr_group, curr_overlap, max_group_size=None):
    global curr_max_groups, seen, max_group_len
    if curr_group in seen:
        return
    if max_group_size and len(curr_group) > max_group_size:
        return
    sub_groups = False
    # print(f"size={len(curr_group)}",end="\r")
    # pivot_bot = None
    # if bots:
    #     pivot_bot = bots[0]
    for idx, b in enumerate(bots):
        if not curr_group:
            print(idx)
        # remaining connections
        other_bot_count = sum(int(ob in overlaps_bots[b]) for ob in bots[idx+1:])
        if other_bot_count < max_group_len - len(curr_group):
            # This is a dead list ...
            break
        b_list = (b,)
        #if b is pivot_bot or b not in overlaps_bots[pivot_bot]:
        if not curr_group or b in overlaps_bots[curr_group[-1]]:


            new_overlap = b + curr_overlap
            if NanobotOverlap.have_overlap(curr_group, overlap=new_overlap):
                sub_groups = True
                # Only consider unconsidered bots
                build_bot_groups(bots[idx+1:] , curr_group + b_list, new_overlap, max_group_size=max_group_size)
    if not sub_groups:
        curr_group_len = len(curr_group)
        if curr_group_len > max_group_len:
            curr_max_groups = set([curr_group])
            max_group_len = len(curr_group) 
            return True
        elif curr_group_len == max_group_len:
            curr_max_groups.add(curr_group)
            print(f"+{len(curr_max_groups)},{max_group_len}", flush=True)
            return True
    seen.add(curr_group)
    return False

        
try:
    # Degeneracy ordering ...
    bots = tuple(sorted(bots, key=overlap_sort, reverse=True))
    build_bot_groups(bots, tuple(), NanobotOverlap())
except KeyboardInterrupt:
    # Gets stuck looking at long paths (960+) even though it probably already found the solution
    pass
print(len(curr_max_groups))

