#!/usr/bin/env python3
# Add current dir to path
from operator import itemgetter
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=3)
puzzle_input = puzzle.get_input()


diag_report = puzzle_input
# Actual Code
oxy_gen_rate = ""
co2_scrub_rate = ""

rate_size = len(diag_report[0])
oxy_bits = list(diag_report)
co2_bits = list(diag_report)
for i in range(rate_size):
    getter = itemgetter(i)

    oxy_rate_at = list(map(getter, oxy_bits))
    most_common_bit =  max(reversed(sorted(set(oxy_rate_at))), key=lambda b: oxy_rate_at.count(b))
    oxy_bits = list(filter(lambda bs: getter(bs) == most_common_bit, oxy_bits))

    co2_rate_at = list(map(getter, co2_bits))
    least_common_bit = min(sorted(set(co2_rate_at)), key=lambda b: co2_rate_at.count(b))
    co2_bits = list(filter(lambda bs: getter(bs) == least_common_bit, co2_bits))

assert len(oxy_bits) == 1 and len(co2_bits) == 1, (oxy_bits, co2_bits)
oxy_gen_rate = oxy_bits[0]
co2_scrub_rate = co2_bits[0]

# Result
print(int(oxy_gen_rate, 2)*int(co2_scrub_rate, 2))