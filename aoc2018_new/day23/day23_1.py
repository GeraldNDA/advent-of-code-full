#!/usr/bin/env python3
# Imports
import re

from aoc import AdventOfCode
# Input Parse
puzzle = AdventOfCode(year=2018, day=23)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "pos=<0,0,0>, r=4",
#     "pos=<1,0,0>, r=1",
#     "pos=<4,0,0>, r=3",
#     "pos=<0,2,0>, r=1",
#     "pos=<0,5,0>, r=3",
#     "pos=<0,0,3>, r=1",
#     "pos=<1,1,1>, r=1",
#     "pos=<1,1,2>, r=1",
#     "pos=<1,3,1>, r=1",
# ]


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
        assert(type(other) is Nanobot)
        return self.distance(other) <= self.radius

    def __gt__(self, other):
        if type(other) is Nanobot:
            return self.radius > other.radius
        raise NotImplementedError
    def __str__(self):
        return f"Nanobot(pos=<{self.pos[0]},{self.pos[1]},{self.pos[2]}>, r={self.radius})"
    @staticmethod
    def parse(line):
        bot_info = Nanobot.NANOBOT_INFO_LINE_MATCHER.match(line)
        if not bot_info:
            raise ValueError(line)
        else:
            bot_info = bot_info.groups()
            return Nanobot(tuple(map(int, bot_info[0:3])), int(bot_info[3]))

# Actual Code
bots = tuple(map(Nanobot.parse, puzzle_input))
largest_range_bot = max(bots)
print(largest_range_bot)

# Result
print(len(tuple(filter(largest_range_bot.in_range,bots))))