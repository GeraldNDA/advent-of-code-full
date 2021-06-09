#!/usr/bin/env python3
# Imports
from typing import List, Tuple, Dict, Text
from typing import Sequence, Union, Optional, Iterable

from math import sqrt
from itertools import product
import re

from aoc import AdventOfCode


# Input Parse
puzzle = AdventOfCode(year=2018, day=23)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "pos=<10,12,12>, r=2",
#     "pos=<12,14,12>, r=2",
#     "pos=<16,12,12>, r=4",
#     "pos=<14,14,14>, r=6", 
#     "pos=<50,50,50>, r=200",
#     "pos=<10,10,10>, r=5",
# ]


class Nanobot(object):
    NANOBOT_INFO_LINE_MATCHER = re.compile(r"pos=<\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*>, r=\s*(-?\d+)\s*")
    IN_RANGE = dict()
    def __init__(self, pos: Tuple[int, int, int], radius: int) -> None:
        self.pos = pos
        self.radius = radius
    
    def distance(self, other: Union['Nanobot', Tuple]) -> int:
        if type(other) is Nanobot:
            other_pos = other.pos
        elif type(other) is tuple and len(other) == 3:
            other_pos = other
        else:
            raise ValueError(other)
        return sum(abs(pos - other_pos[idx]) for idx, pos in enumerate(self.pos))

    def in_range(self, other: Union['Nanobot', Tuple]) -> bool:
        return self.distance(other) <= self.radius
    
    def __contains__(self, other: Union['Nanobot', Tuple]) -> bool:
        return self.in_range(other)

    def __gt__(self, other: 'Nanobot') -> bool:
        if type(other) is Nanobot:
            return self.radius > other.radius
        raise NotImplementedError
    
    def __repr__(self):
        return f"Nanobot(pos=<{self.pos[0]},{self.pos[1]},{self.pos[2]}>, r={self.radius})"
    
    def bots_in_range(self, bots: Sequence['Nanobot']) -> int:
        bots_in_range = 0
        for bot in bots:
            if self.in_range(bot):
                bots_in_range += 1
        return bots_in_range

    @staticmethod
    def parse(line: Text) -> 'Nanobot':
        bot_info = Nanobot.NANOBOT_INFO_LINE_MATCHER.match(line)
        if not bot_info:
            raise ValueError(line)
        else:
            bot_info = bot_info.groups()
            return Nanobot(tuple(map(int, bot_info[0:3])), int(bot_info[3]))

class NanobotRange:
    def __init__(self, ranges: Sequence[Tuple[Optional[int], Optional[int]]]=None, made_points: Optional[bool]=None) -> None:
        self.ranges: List[Tuple[Optional[int], Optional[int]]] = ranges or [(None, None)]*3
        if len(self.ranges) != 3 or len(self.ranges[0]) != 2:
            raise ValueError
        self.is_point = made_points
        if made_points or made_points is None:
            self.is_point = all(None not in dim and dim[1] == dim[0] for dim in self.ranges)

    @staticmethod
    def from_bot(bot: Nanobot) -> 'NanobotRange':
        return NanobotRange(ranges=[(dim - bot.radius, dim + bot.radius) for dim in bot.pos])

    def __iter__(self):
        for x in range(self.ranges[0][0], self.ranges[0][1] + 1):
            for y in range(self.ranges[1][0], self.ranges[1][1] + 1):
                for z in range(self.ranges[2][0], self.ranges[2][1] + 1):
                    yield (x, y, z)

    def center(self) -> Tuple[int]:
        return tuple(sum(range)//2 for range in self.ranges)

    def distance_from_center(self) -> int:
        return sum(abs(dim) for dim in self.center())

    def __bool__(self) -> bool:
        return not all(curr_range == (None, None) for curr_range in self.ranges)

    def __or__(self, other: 'NanobotRange') -> 'NanobotRange':
        if not self and not other:
            return NanobotRange()
        if not self:
            return NanobotRange(ranges=list(other.ranges))
        if not other:
            return NanobotRange(ranges=list(self.ranges))
        return NanobotRange(ranges=[
            (min(self_range[0], other_range[0]), max(self_range[1], other_range[1])) for self_range, other_range in zip(self.ranges, other.ranges)
        ])


    def distance_from_bot(self, bot: Nanobot) -> float:
        distance = 0
        for dim, edge in zip(bot.pos, self.ranges):
            distance += max(edge[0] - dim, 0, dim - edge[1])**2
        return sqrt(distance)

    def intersects(self, bot: Nanobot) -> bool:
        return self.distance_from_bot(bot) <= bot.radius

    def is_valid(self):
        return all(curr_range[0] <= curr_range[1] for curr_range in self.ranges)

    def size(self):
        size = 1
        for dim in self.ranges:
            size *= (dim[1] - dim[0] + 1)
        return size

    def __contains__(self, bot: Nanobot) -> bool:
        # First check if pos is in range
        if self.is_point:
            return tuple(pos[0] for pos in self.ranges) in bot

        # Convert bot to range and perform an intersection
        return self.intersects(bot)

    def __repr__(self) -> str:
        return f"NanobotRange(ranges={self.ranges})"

    def split(self) -> Sequence['NanobotRange']:
        if self.is_point:
            return [self]
        made_points = False
        lengths = [curr_range[1] - curr_range[0] for curr_range in self.ranges]
        max_dim = max(range(3), key=lambda d: lengths[d])
        max_dim_size = lengths[max_dim]
        max_dim_range = self.ranges[max_dim]
        if max_dim_size > 1:
            center = self.center()
            new_bot = max_dim_range[0], center
            new_top = center, max_dim_range[1]
        else:
            new_bot = max_dim_range[0], max_dim_range[0]
            new_top = max_dim_range[1], max_dim_range[1]
            made_points = True

        top_range, bot_range = NanobotRange(ranges=list(self.ranges), made_points=made_points), NanobotRange(ranges=list(self.ranges), made_points=made_points)
        bot_range.ranges[max_dim] = new_bot
        top_range.ranges[max_dim] = new_top
        return [top_range, bot_range]

    def split_even(self) -> Sequence['NanobotRange']:
        old_list = [self]
        new_list = []
        for _ in range(3):
            for curr_range in old_list:
                new_list.extend(curr_range.split())
            old_list, new_list = new_list, []
        return old_list

    def split_pivot(self, bots: List[Nanobot]) -> List['NanobotRange']:
        if self.is_point:
            raise ValueError("Can't split a point")
        
        # Find widest range
        for idx, curr_range in sorted(enumerate(self.ranges), key=lambda r: r[1][1] - r[1][0]):
            lower_bound, upper_bound = curr_range
            lower_box, mid_box, upper_box = list(self.ranges), list(self.ranges), list(self.ranges)
            pivot = sum(curr_range)//2
            # if the range can be split such that one has more bots, then perform that split
            if upper_bound - lower_bound > 2:
                lower_box[idx] = lower_bound, pivot
                upper_box[idx] = pivot+1, upper_bound
                
                lower_range = NanobotRange(ranges=lower_box)
                upper_range = NanobotRange(ranges=upper_box)
                in_lower, in_upper = 0, 0
                for bot in bots:
                    if bot in lower_range:
                        in_lower += 1
                    if bot in upper_range:
                        in_upper += 1
                if in_lower != in_upper:
                    ranges = [NanobotRange(ranges=(lower_box if in_lower > in_upper else upper_box))]
                    # print(f"DID BIG SLICE ({in_lower} -> {lower_box}) vs ({in_upper} -> {upper_box}) = {ranges}")
                    return ranges
            elif upper_bound != lower_bound:

                lower_box[idx] = lower_bound, lower_bound
                mid_box[idx] = pivot, pivot
                upper_box[idx] = upper_bound, upper_bound
                lower_range = NanobotRange(ranges=lower_box)
                mid_range = NanobotRange(ranges=mid_box)
                upper_range = NanobotRange(ranges=upper_box)
                in_lower, in_mid, in_upper = 0, 0, 0
                for bot in bots:
                    if bot in lower_range:
                        in_lower += 1
                    if bot in mid_range:
                        in_mid += 1
                    if bot in upper_range:
                        in_upper += 1
                most = max(in_lower, in_mid, in_upper)
                ranges = [lower_range, mid_range, upper_range]
                if in_lower == in_mid == in_upper:
                    # print(f"MADE 'POINT' ALL -> {ranges}")
                    return ranges
                else:
                    # print("L", lower_range)
                    # print("M", mid_range)
                    # print("U", upper_range)
                    # for bot in bots:
                    #     print(bot,"|", NanobotRange.from_bot(bot), end=" ")
                    #     if bot in lower_range:
                    #         print("L", end=" ")
                    #     if bot in mid_range:
                    #         print("M", end=" ")
                    #     if bot in upper_range:
                    #         print("U", end=" ")
                    #     print()
                    #     print(f"bot^mid_range={mid_range ^ bot}")
                    ranges = [ranges[idx] for idx, in_bots in enumerate((in_lower, in_mid, in_upper)) if in_bots == most]
                    # print(f"MADE 'POINT' SOME -> {ranges}")
                    return ranges

        else:
            max_dim, max_range = max(enumerate(self.ranges), key=lambda r: r[1][1] - r[1][0])
            lower_bound, upper_bound = max_range
            lower_box, upper_box = list(self.ranges),  list(self.ranges)
            pivot = sum(curr_range)//2
            lower_box[max_dim] = lower_bound, pivot
            upper_box[max_dim] = pivot+1, upper_bound
            lower_range, upper_range = NanobotRange(ranges=lower_box), NanobotRange(ranges=upper_box)
            at_lower, at_upper = 0, 0
            for bot in bots:
                if lower_range.center() in bot:
                    at_lower += 1
                if upper_range.center() in bot:
                    at_upper += 1
            if at_lower != at_upper:
                return [lower_range if at_lower > at_upper else upper_range]
            # print("SPLIT 50/50",tuple((cr, sum((bot in cr) for bot in bots)) for cr in ranges))
            return [lower_range, upper_range]


        # Otherwise this range cannot be split in any way
        raise ValueError(f"Couldn't find a valid split for {self}")



bots: Tuple[Nanobot] = tuple(Nanobot.parse(line) for line in puzzle_input)
initial_ranges: List[NanobotRange] = [NanobotRange()]
for bot in bots:
    initial_ranges[0] |= NanobotRange.from_bot(bot)
best_point: Optional[NanobotRange] = None
best_point_bots = 0
while initial_ranges:
    new_ranges = []
    max_bots = best_point_bots
    print(len(initial_ranges), sum(dim[1] - dim[0] for dim in initial_ranges[0].ranges))
    for initial_range in initial_ranges:
        assert initial_range.is_valid(), f"{initial_range}"
        # print(f"{sum(dim[1] - dim[0] for dim in initial_range.ranges)}", " "*30)
        try:
            for new_range in initial_range.split_pivot(bots):
                in_new = sum((bot in new_range) for bot in bots)
                max_bots = max(max_bots, in_new)
                if new_range.is_point:
                    if best_point is None:
                        print("FRESH BEST")
                        best_point = new_range
                        best_point_bots = in_new

                    elif in_new > best_point_bots:
                        print("NEW BEST")
                        best_point = new_range
                        best_point_bots = in_new
                    elif in_new == best_point_bots and new_range.distance_from_center() < best_point.distance_from_center():
                        print("CLOSER BEST")
                        best_point = new_range
                        best_point_bots = in_new
                else:
                    new_ranges.append((in_new, new_range))
        except ValueError:
            print(f"Looping through all {initial_range.size()}")
            idx = 0
            for point in initial_range:
                assert idx < initial_range.size()
                idx += 1
                print(f"Looking at point {idx}", end="\r")
                in_new = sum(point in bot for bot in bots)
                point = NanobotRange(list(zip(point, point)), made_points=True)
                assert point.is_point
                if best_point is None:
                    print("FRESH BEST", point, in_new)
                    best_point = point
                    best_point_bots = in_new
                elif in_new > best_point_bots:
                    print("NEW BEST")
                    best_point = point
                    best_point_bots = in_new
                elif in_new == best_point_bots and point.distance_from_center() < best_point.distance_from_center():
                    print("CLOSER BEST")
                    best_point = new_range
                    best_point_bots = in_new
    # assert not new_ranges or any(Nanobot((12,12,12), 0) in new_range for _, new_range in new_ranges), f"{initial_ranges} -> {new_ranges}"
    initial_ranges = [new_range for in_range, new_range in new_ranges if in_range >= max_bots]
print(best_point)
print(best_point_bots)