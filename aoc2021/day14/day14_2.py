#!/usr/bin/env python3
# Add current dir to path
from abc import ABC
from os import times
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from collections import Counter
from operator import methodcaller
from functools import lru_cache

# Input Parse
puzzle = AdventOfCode(year=2021, day=14)
puzzle_input = puzzle.get_input()

puzzle_input = iter(puzzle_input)
polymer_template = next(puzzle_input)
next(puzzle_input) # blank_Line

insertion_rule = {pair: to_insert for pair, to_insert in map(methodcaller("split", " -> "), puzzle_input)}

solutions = {}
def solve_insertion(start, end, max_iters=None):
    pair = "".join((start, end))
    template = pair
    iters = 0
    new_template = [template[0]]
    while pair not in template:
        for new_pair in zip(template[:-1], template[1:]):
            new_template.extend((insertion_rule["".join(new_pair)], new_pair[-1]))
        template = "".join(new_template)
        iters += 1
        if max_iters and iters >= max_iters:
            solutions[start, end] = None
            return
    solutions[start, end] = (template, iters)

for pair in zip(polymer_template[:-1], polymer_template[1:]):
    solve_insertion(*pair, None)
print(list(solutions.keys()))
print(len(polymer_template))
# solutions = {pair: solve_insertion(*pair) for pair in insertion_rule}

# for pair, solution in solutions.items():
#     if solution is None:
#         print(pair, "->", [p for p, s in solutions.items() if s and pair in s], pair in polymer_template)

# # Actual Code
# cache ={}
# xX = Counter()
# def find_elem_counts(start, end, iters, parents=set()):

#     if iters == 0:
#         return Counter((start, end))

#     pair = "".join((start, end))
#     to_insert  = insertion_rule[pair]
#     print("="*iters, " "*(TOTAL_ITERS-iters), start, end, "->", to_insert)
#     xX[start, end] += 1
#     expanded  = (start, to_insert, end)

#     if len(set(expanded[1:])) != len(set(expanded[:-1])):
#         repeat_pair = min(expanded[1:], expanded[:-1], key=lambda p: len(set(p)))
#         order_pair = max(expanded[1:], expanded[:-1], key=lambda p: len(set(p)))
#         elem_counts = Counter()
#         for new_iter in range(iters):
#             elem_counts += find_elem_counts(*repeat_pair, new_iter) - Counter(to_insert)
#         elem_counts += Counter(order_pair)
#         cache[start, end, iters] = elem_counts
#         return elem_counts

#     elem_counts = find_elem_counts(*expanded[:-1], iters-1) + find_elem_counts(*expanded[1:], iters-1) - Counter(to_insert)
#     cache[start, end, iters] = elem_counts
#     return elem_counts

# def count_template(template, iters):
#     element_counts = Counter(template[0])
#     for pair in zip(template[:-1], template[1:]):
#         element_counts += find_elem_counts(*pair, iters) - Counter(pair[0])


# solutions = {}
# def find_elem_counts(start, end, iters):

#     pair = "".join((start, end))
#     template = pair
#     new_template = [template[0]]
#     for remaining_iter in reversed(range(iters)):
#         for new_pair in zip(template[:-1], template[1:]):
#             new_template.extend((insertion_rule["".join(new_pair)], new_pair[-1]))
#         template = "".join(new_template)
#         if pair in template:
#             # "Solved" a part of it, we know the counts up until a certain amount, and can just calculate a smaller one
#             solutions[pair] = lambda i: Counter({start: })
#     solutions[start, end] = (template, iters)
#     return template

# goal = 10
# AB
# AZB
# A0Z1B 
# AD0CZB1AB AB(iter=3)
# (iter=6)
# AD (iter3)
# D0 (iter3)
# CZ (iter3)
# ZB (iter3)
# B1 (iter3)
# 1A (iter3)
# AB (iter3) => Known = blah blah blah
# (iter=9)
# AD (iter6)
# D0 (iter6)
# CZ (iter6)
# ZB (iter6)
# B1 (iter6)
# 1A (iter6)
# AB (iter6) => Known = 

# 0CZB1AB 


# # TOTAL_ITERS = 6
# element_counts = Counter(polymer_template[0])
# for pair in zip(polymer_template[:-1], polymer_template[1:]):
#     element_counts += find_elem_counts(*pair, TOTAL_ITERS) - Counter(pair[0])

# print(xX)

# Result
# print(max(element_counts.values()) - min(element_counts.values()))