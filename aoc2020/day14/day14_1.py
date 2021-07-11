#!/usr/bin/env python3
# Add current dir to path
import code
import re
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2020, day=14)
puzzle_input = puzzle.get_input()


class Mask:
    def __init__(self, mask):
        self.and_mask = Mask.to_and(mask)
        self.or_mask = Mask.to_or(mask)

    @staticmethod
    def to_and(mask):
        # AND'ing with this mask forces zeros in correct locations
        return int(mask.replace("X", "1"), 2)
    
    @staticmethod
    def to_or(mask):
        # OR'ing with this mask forces ones in correct locations
        return int(mask.replace("X", "0"), 2)

    def apply(self, num):
        return (num & self.and_mask) | self.or_mask

class InitProgram:
    MASK_LINE = re.compile(r"mask = (?P<mask>[01X]{36})")
    MEM_LINE = re.compile(r"mem\[(?P<addr>\d+)\] = (?P<value>\d+)")

    def __init__(self) -> None:
        self.curr_mask = None
        self.memory = {}

    def set_mask(self, mask):
        self.curr_mask = mask

    def update_mem(self, addr, value):
        self.memory[addr] = self.curr_mask.apply(value)

    def apply_line(self, line):
        mask_match = InitProgram.MASK_LINE.match(line)
        mem_match = InitProgram.MEM_LINE.match(line)
        
        if mask_match:
            assert mem_match is None
            self.set_mask(Mask(mask_match.group("mask")))


        if mem_match:
            self.update_mem(int(mem_match.group("addr")), int(mem_match.group("value")))

# Actual Code
program = InitProgram()
for line in puzzle_input:
    program.apply_line(line)

# Result
print(sum(program.memory.values()))
