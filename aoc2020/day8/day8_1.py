#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller
# Input Parse
puzzle = AdventOfCode(year=2020, day=8)
puzzle_input = puzzle.get_input()

class GameConsole:
    def __init__(self, code) -> None:
        self.code = self.decode(code)
        self.pc = 0
        self.acc = 0

    def decode(self, code):
        return [(getattr(self, instr), int(param)) for instr, param in map(methodcaller("split", " "), code)]

    def nop(self, _):
        pass

    def acc(self, param):
        self.acc  += param

    def jmp(self, param):
        self.pc += param - 1

    def run(self):
        while self.pc < len(self.code):
            instr, param = self.code[self.pc]
            instr(param)
            self.pc += 1
            yield self.pc

# Actual Code
console = GameConsole(puzzle_input)
seen = set()
for pc in console.run():
    if pc in seen:
        print(console.acc)
        break
    seen.add(pc)
