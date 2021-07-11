0#!/usr/bin/env python3
# Add current dir to path
from functools import reduce
from itertools import starmap
import operator
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from math import gcd
# Input Parse
puzzle = AdventOfCode(year=2020, day=13)
puzzle_input = puzzle.get_input()

depart_time = int(puzzle_input[0])
busses = tuple(map(lambda bus_id: int(bus_id) if bus_id != "x" else None, puzzle_input[1].split(",")))

def assert_pairwise_coprime(nums):
    for idx, num in enumerate(nums):
        for other_num in nums[idx+1:]:
            assert gcd(num, other_num) == 1, f"{num} and {other_num} are not coprime"

def egcd(a, b):
    """
    returns gcd(a,b) and x, y solution to gcd(a, b) = ax + by
    based on wiki solution
    """
    prev_r, r = (a, b) if a > b else (b, a)
    prev_x, x = 1, 0
    prev_y, y = 0, 1

    while r:
        q = prev_r // r
        prev_r, r = r, prev_r - q*r
        prev_x, x = x, prev_x - q*x
        prev_y, y = y, prev_y - q*y

    return prev_r, prev_x, prev_y

def mod_inv(a, n):
    # solve for x in ax === r (mod n)
    # a and n should be coprime
    gcd_result, x, _ = egcd(a, n)
    assert gcd_result == 1
    return x % n

def chinese_remainder(nums, remainders):
    """
    solves for x in:
    x = remainder[i] (mod nums[i])
    for all i in [0, len(nums))
    """
    assert_pairwise_coprime(nums)
    N = reduce(operator.mul, nums)
    A = tuple(reduce(operator.mul, nums[:i] + nums[i+1:]) for i in range(len(nums)))
    # solve A[i]*x[i] = 1 (mod nums[i])
    x = tuple(starmap(mod_inv ,zip(A, nums)))
    return sum(map(lambda t: reduce(operator.mul, t), zip(x, A, remainders))) % N

# Actual Code
nums, remainders = zip(*((bus, (-idx) % bus) for idx, bus in enumerate(busses) if bus is not None))
start_time = chinese_remainder(nums, remainders)

# Result
print(start_time)