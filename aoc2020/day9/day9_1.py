#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
from typing import OrderedDict
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

import operator
from collections import defaultdict
# Input Parse
puzzle = AdventOfCode(year=2020, day=9)
puzzle_input = puzzle.get_input()

# Actual Code
XMAS = map(int, puzzle_input)


class PrevOpCache:
    # Assumes no duplicates, if there are duplicates, you'd need to not use set for the cache, probably would have to use lists
    def __init__(self, op, max) -> None:
        self.seen = []
        self.cache = defaultdict(set)
        self.op = op
        self.max = max

    def add(self, num):
        for prev_num in self.seen[-self.max:]:
            self.cache[self.op(num, prev_num)].add((prev_num, num))
        self.seen.append(num)
        if len(self.seen) > self.max:
            self._pop()
        

    def _pop(self):
        top_idx = -(self.max+1)
        top = self.seen[top_idx]
        for post_num in self.seen[-self.max:]:
            self.cache[self.op(post_num, top)].remove((top, post_num))

    def check(self, num):
        if len(self.seen) < self.max:
            return False
        return bool(self.cache[num])

    def __len__(self):
        return min(self.max, len(self.seen))


cache = PrevOpCache(operator.add, 25)
for num in XMAS:
    if len(cache) == 25 and not cache.check(num):
            print(num)
            break
    cache.add(num)
