#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from collections import defaultdict, OrderedDict

# Input Parse
puzzle = AdventOfCode(year=2018, day=7)
puzzle_input = puzzle.get_input()

def parse_dependency(line):
    line = line.split()
    if line:
        return (line[1], line[-3])
step_relations = map(parse_dependency, puzzle_input)
order = ""
# Actual Code
in_degree_map  = defaultdict(int)
connection_map = defaultdict(list)
for step_relation in step_relations:
    in_degree_map[step_relation[1]] += 1
    in_degree_map[step_relation[0]] += 0
    connection_map[step_relation[0]].append(step_relation[1])

in_degree_map = OrderedDict(sorted(in_degree_map.items()))

while in_degree_map:
    min_in_deg = min(in_degree_map, key=lambda sr: in_degree_map[sr])
    in_degree = in_degree_map.pop(min_in_deg)
    if in_degree != 0:
        raise ValueError("CAN'T DO ALL STEPS , min degree is %d" % in_degree)
    order += min_in_deg
    for item in connection_map[min_in_deg]:
        in_degree_map[item] -= 1

# Result
print(order)