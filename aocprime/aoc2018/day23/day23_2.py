#!/usr/bin/env python3
# Imports
from space import Bounds, ManhattanSphere, SignalSpace
from typing import Optional, List, Text, Tuple
from typing import NamedTuple
from functools import reduce

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

class Nanobot(ManhattanSphere):
    NANOBOT_INFO_LINE_MATCHER = re.compile(r"pos=<\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*>, r=\s*(-?\d+)\s*")
    IN_RANGE = dict()

    @staticmethod
    def parse(line: Text) -> 'Nanobot':
        bot_info = Nanobot.NANOBOT_INFO_LINE_MATCHER.match(line)
        if not bot_info:
            raise ValueError(line)
        else:
            bot_info = bot_info.groups()
            return Nanobot(tuple(map(int, bot_info[0:3])), int(bot_info[3]))

class NanobotRange(SignalSpace):
    @staticmethod
    def from_bot(bot: Nanobot) -> 'NanobotRange':
        return NanobotRange(tuple([Bounds(dim - bot.radius, dim + bot.radius) for dim in bot.centre]))

    def is_point(self) -> bool:
        return all(edge.lower_bound == edge.upper_bound for edge in self.edges)

    def origin_distance(self) -> int:
        return sum(abs(sum(edge)//2) for edge in self.edges)

    def __contains__(self, other: Nanobot) -> bool:
        if not isinstance(other, Nanobot):
            return NotImplemented
        return self.contains(other)

    def __lt__(self, other: "NanobotRange") -> bool:
        if not isinstance(other, NanobotRange):
            return NotImplemented
        return self.origin_distance() < other.origin_distance()

    def __repr__(self):
        return f"NanobotRange({self.edges})"

class SearchNode(NamedTuple):
    space: Optional[SignalSpace] = None
    bots: Tuple[Nanobot] = tuple()

    def split(self):
        # search for pivot in each dimension and split from there
        midpoints = []
        # Find which dimension can be split
        for dim, edge in enumerate(self.space.edges):
            mid = edge.midpoint()
            top, bottom = self.space.slice(dim, mid)
            in_top = tuple(filter(lambda b: b in top, self.bots))
            in_bottom = tuple(filter(lambda b: b in bottom, self.bots))
            while in_top == in_bottom and edge.lower_bound < edge.upper_bound:
                edge = Bounds(edge.lower_bound, mid)
                mid = edge.midpoint()
                top, bottom = self.space.slice(dim, mid)
                in_top = tuple(filter(lambda b: b in top, self.bots))
                in_bottom = tuple(filter(lambda b: b in bottom, self.bots))
            midpoints.append(mid)
        yield from self.space.split(tuple(midpoints))

    def fit_bots(self):
        bot_space = SearchNode.to_space(self.bots)
        if bot_space is None:
            return
        for idx, (space_edge, bot_edge) in enumerate(zip(self.space.edges, bot_space.edges)):
            self.space.edges[idx] = Bounds(
                max(space_edge.lower_bound, bot_edge.lower_bound), # use tightest bound
                min(space_edge.upper_bound, bot_edge.upper_bound), # use tightest bound
            )

    def size(self):
        if self.space is None:
            return 0
        return reduce(lambda size, edge: size*max(1, edge.upper_bound - edge.lower_bound),  self.space.edges, 1)

    @staticmethod
    def to_space(bots):
        return reduce(lambda acc, bot: NanobotRange.from_bot(bot).merge(acc), bots, None)

# Strategy:
# 1. Create search space from all bots
# 2. Try to shrink space as much as possible
# 3. Try to re-add bots 1-by-1


bots: Tuple[Nanobot] = tuple(Nanobot.parse(line) for line in puzzle_input)
search_front: List[SearchNode] = [SearchNode(SearchNode.to_space(bots), bots)]
best_node: SearchNode = SearchNode(None, tuple())

while search_front:
    curr_node = search_front.pop(0)
    print(len(search_front), curr_node.size(), len(curr_node.bots))
    to_add = []
    # print(curr_node.space)
    # print("="*20)
    max_num_bots = 0
    for subspace in curr_node.split():
        bots = tuple(filter(lambda b: b in subspace, curr_node.bots))
        num_bots = len(bots)
        if num_bots == 0:
            continue
        # print(subspace)
        # print(num_bots)
        if subspace.is_point():
            if num_bots > len(best_node.bots) or (num_bots == len(best_node.bots) and subspace < best_node.space):
                best_node = SearchNode(subspace, bots)
                print(subspace, num_bots, " "*100)
        else:
            if num_bots >= len(best_node.bots):
                if num_bots > max_num_bots:
                    to_add = [SearchNode(subspace, bots)]
                    max_num_bots = num_bots         
                elif num_bots == max_num_bots:
                    node = SearchNode(subspace, bots)
                    if node not in to_add:
                        to_add.append(node)
    to_add.sort(reverse=True, key=lambda n: len(n.bots))
    if to_add:
        print("s", len(search_front), len(curr_node.bots), len(to_add))
    search_front = to_add + search_front
print(best_node.space)
# print(sum(x))