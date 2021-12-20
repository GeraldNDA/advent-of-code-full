#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from itertools import permutations
from operator import methodcaller

# Input Parse
puzzle = AdventOfCode(year=2021, day=18)
puzzle_input = puzzle.get_input()

# Actual Code
def round_down(n, div):
    return n // div

def round_up(n, div):
    return (n + div - 1) // div

class SnailFish:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def __add__(self, other):
        assert type(other) is SnailFish or other == 0
        if not other:
            return self
        return SnailFish(self.copy(), other.copy()).reduce()

    def __radd__(self, other):
       return self + other

    def reduce(self):
        reduced = True
        while reduced:
            reduced = self.explode()
            if not reduced:
                reduced = self.split()
            # print(f"-> {self} | reduced={reduced}")
        return self

    def explode(self, parents=tuple()):
        # print(f"EXPLODE {self}")
        # print(self, len(parents))
        if len(parents) == 4:
            assert all((type(subf) is int) for subf in (self.left, self.right))
            self.apply_explode(parents)
            return True
        if type(self.left) is SnailFish:
            if self.left.explode(parents=(self,)+parents):
                return True
        if type(self.right) is SnailFish:
            if self.right.explode(parents=(self,)+parents):
                return True
        return False

    def apply_explode(self, parents):
        # Will be in order going TOWARDS root
        exploded_left, exploded_right = False, False
        self_branch = parents + (self,)
        for parent in parents:
            # Find the right most element in the left parents' and the opposite for right
            if not exploded_left and parent.left not in self_branch:
                if type(parent.left) is int:
                    parent.left += self.left
                    exploded_left = True
                else:
                    exploded_left = parent.left.apply_explode_right(self.left)
            if not exploded_right and parent.right not in self_branch:
                if type(parent.right) is int:
                    parent.right += self.right
                    exploded_right = True
                else:
                    exploded_right = parent.right.apply_explode_left(self.right)
        if parents[0].left is self:
            parents[0].left = 0
        elif parents[0].right is self:
            parents[0].right = 0
        else:
            assert False, "Parents didn't match expectation?!"

    def copy(self):
        left_fish = self.left if type(self.left) is int else self.left.copy()
        right_fish = self.right if type(self.right) is int else self.right.copy()
        return SnailFish(left_fish, right_fish)

    def apply_explode_left(self, value):
        if type(self.left) is int:
            self.left += value
            return True
        # Find right most element of left tree and then do that
        return self.left.apply_explode_left(value)
        
    def apply_explode_right(self, value):
        if type(self.right) is int:
            self.right += value
            return True
        return self.right.apply_explode_right(value)

    def split(self):
        # print(f"SPLIT {self}")

        if type(self.left) is int and self.left >= 10:
            self.left = SnailFish(round_down(self.left, 2), round_up(self.left, 2))
            return True
        elif type(self.left) is SnailFish:
            if self.left.split():
                return True
        
        if type(self.right) is int and self.right >= 10:
            self.right = SnailFish(round_down(self.right, 2), round_up(self.right, 2))
            return True
        elif type(self.right) is SnailFish:
            if self.right.split():
                return True
        return False

    def magnitude(self):
        left_magnitude = self.left if type(self.left) is int else self.left.magnitude()
        right_magnitude = self.right if type(self.right) is int else self.right.magnitude()
        return 3*left_magnitude + 2*right_magnitude

    @staticmethod
    def from_pair(left, right):
        def sub_decode(subfish):
            if type(subfish) is int:
                return subfish
            if type(subfish) is list:
                assert len(subfish) == 2
                return SnailFish.from_pair(*subfish)
            assert False, "Invalid subfish type"
        return SnailFish(sub_decode(left), sub_decode(right))
        
    @staticmethod
    def parse(fishstr):
        fishpair = eval(fishstr)
        assert type(fishpair) is list and len(fishpair) == 2
        return SnailFish.from_pair(*fishpair)

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"

school = map(SnailFish.parse, puzzle_input)
# Result
print(max(
    map(methodcaller("magnitude"), 
        map(sum, permutations(school, 2))
    )
))