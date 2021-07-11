#!/usr/bin/env python3
# Add current dir to path
from dataclasses import Field
from functools import reduce
from operator import itemgetter, methodcaller
import operator
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=16)
puzzle_input = puzzle.get_input()

class FieldRule(NamedTuple):
    start: int
    end: int

    def __contains__(self, field_value):
        return field_value in range(self.start, self.end+1)

    @staticmethod
    def parse(rule_string):
        return FieldRule(*map(int, rule_string.split("-")))

class TicketRule:

    def __init__(self) -> None:
        self.rules: Dict[str, Tuple[FieldRule]] = {}

    def passing(self, field_value):
        return tuple(filter(lambda rule_name: any((field_value in rule) for rule in self.rules[rule_name]), self.rules.keys()))

    @staticmethod
    def parse(rule_stream):
        rule_set = TicketRule()
        for rule in rule_stream:
            if not rule:
                break
            rule_name, rules = rule.split(":")
            rules = tuple(map(FieldRule.parse, rules.strip().split(" or ")))
            rule_set.rules[rule_name] = rules
        return rule_set

class Ticket:
    SECTION_MARKERS = ["your ticket:", "nearby tickets:"]
    def __init__(self, field_values) -> None:
        self.ticket: Tuple[int] = field_values

    @staticmethod
    def parse(ticket_stream):
        for ticket in ticket_stream:
            if not ticket:
                break
            if ticket in Ticket.SECTION_MARKERS:
                continue
            yield Ticket(tuple(map(int, ticket.split(","))))

    def valid_ticket(self, rules):
        return all(bool(rules.passing(field)) for field in self.ticket)

    def get_error_rate(self, rules):
        return sum(field for field in self.ticket if not rules.passing(field))


ticket_info_stream = (line for line in puzzle_input)
rules = TicketRule.parse(ticket_info_stream)
my_ticket = tuple(Ticket.parse(ticket_info_stream))[0]
nearby_tickets = tuple(Ticket.parse(ticket_info_stream))


# Actual Code
nearby_tickets = tuple(filter(methodcaller("valid_ticket", rules), nearby_tickets))
field_possibilities = [set(rules.rules.keys()) for _ in range(len(rules.rules))]
for ticket in nearby_tickets:
    for idx, field in enumerate(ticket.ticket):
        field_possibilities[idx] &= set(rules.passing(field))

rule_idxs = {}
done = False
while any(field_possibilities):
    for idx, possibilities in enumerate(field_possibilities):
        if len(possibilities) == 1:
            possibilities = possibilities.copy()
            for other_possibilities in field_possibilities:
                other_possibilities -= possibilities
            rule_idxs[possibilities.pop()] = idx

# print(rule_idxs)

# Result
print(reduce(operator.mul, map(my_ticket.ticket.__getitem__, (rule_idx for rule, rule_idx in rule_idxs.items() if rule.startswith("departure")))))
