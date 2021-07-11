#!/usr/bin/env python3
# Add current dir to path
import code
import enum
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
        self.mask = mask

    def apply(self, num):
        as_bin = list(f"{num:036b}")
        for i, mask_bit in enumerate(self.mask):
            if mask_bit in "1X":
                as_bin[i] = mask_bit
        return "".join(as_bin)

class MemNode:
    def __init__(self, bit) -> None:
        self.bit = bit
        self.children = {}

    # Could support "on demand splitting" when a region is being overriten, but that may be too expensive
    #  most number of Xs is 9 (512 entries), so probably better to just list them out

class Memory:
    def __init__(self) -> None:
        self.mem_root = MemNode("")

    def __setitem__(self, key, value):
        nodes = [(0, self.mem_root)]
        while nodes:
            idx, node = nodes.pop(0)
            if not isinstance(node, MemNode):
                continue
            bits = key[idx]
            if bits == "X":
                bits = "01"
            for bit in bits:
                if idx < len(key) - 1:
                    node.children.setdefault(bit, MemNode(bit))
                else:
                    node.children[bit] = value

            for child in map(node.children.get, bits):
                nodes.append((idx+1, child))

    def values(self):
        nodes = [self.mem_root]
        while nodes:
            node = nodes.pop()
            if not isinstance(node, MemNode):
                yield node
            else:
                nodes.extend(node.children.values())

    def items(self):
        nodes = [("", self.mem_root)]
        while nodes:
            key, node = nodes.pop()
            if not isinstance(node, MemNode):
                yield key, node
            else:
                nodes.extend((key+child_key, child_node) for child_key, child_node in node.children.items())

class InitProgram:
    MASK_LINE = re.compile(r"mask = (?P<mask>[01X]{36})")
    MEM_LINE = re.compile(r"mem\[(?P<addr>\d+)\] = (?P<value>\d+)")

    def __init__(self) -> None:
        self.curr_mask = None
        self.memory = Memory()

    def set_mask(self, mask):
        self.curr_mask = mask

    def update_mem(self, addr, value):
        self.memory[self.curr_mask.apply(addr)] = value

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
