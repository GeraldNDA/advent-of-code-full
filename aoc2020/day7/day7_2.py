#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

import re

# Input Parse
puzzle = AdventOfCode(year=2020, day=7)
puzzle_input = puzzle.get_input()


class NestedBags:
    _BAGS = {}
    RULE_DESC = re.compile(r"(?P<bag>[\w\s]+) bags contain (?P<contents>no other bags|(?:\d+ [\w\s]+(?:, \d+ [\w\s]+)*))\.")
    CONTENT_DESC = re.compile(r"(?P<amount>\d+) (?P<bag>[\w\s]+) bags?")

    def __new__(cls, color):
        if color not in cls._BAGS:
            cls._BAGS[color] = super().__new__(cls)
        return cls._BAGS[color]

    def __init__(self, color):
        self.color = color
        if not hasattr(self, "inner_bags"):
            self.inner_bags = {}

    def add(self, bag, amount):
        self.inner_bags[bag] = amount

    def count_contents(self):
        return sum((bag.count_contents()+1)*amount for bag, amount in self.inner_bags.items())

    # def count_of(self, color):
    #     if self.color == color:
    #         return 1
    #     return sum(inner_bag.count_of(color)*amount for inner_bag, amount in self.inner_bags.items())

    @staticmethod
    def parse_rule(rule):
        rule_desc = NestedBags.RULE_DESC.match(rule)
        if not rule_desc:
            return
        bag = NestedBags(rule_desc.group("bag"))
        if rule_desc.group("contents") != "no other bags":
            for content_desc in NestedBags.CONTENT_DESC.finditer(rule_desc.group("contents")):
                bag.add(NestedBags(content_desc.group("bag")), int(content_desc.group("amount")))
        return bag

# Actual Code
set(map(NestedBags.parse_rule, puzzle_input))
print(NestedBags("shiny gold").inner_bags)

# Result
print(NestedBags("shiny gold").count_contents())
