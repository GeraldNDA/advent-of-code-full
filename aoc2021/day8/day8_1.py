#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller
from typing import List

# Input Parse
puzzle = AdventOfCode(year=2021, day=8)
puzzle_input = puzzle.get_input()


# Actual Code
class Signal:
    def __init__(self, signal_patterns: List[str], output_value: List[str]) -> None:
        self.signal_patterns = signal_patterns
        self.output_value = output_value

    def num_easy_outputs(self):
        num_easy = 0
        for n in self.output_value:
            if len(n) in (2, 4, 3, 7):
                num_easy += 1
        return num_easy

    @staticmethod
    def parse(signal_line:str):
        return Signal(*map(methodcaller("split", " "), signal_line.split(" | ")))




signals = map(Signal.parse, puzzle_input)
num_easy_digits = sum(map(methodcaller("num_easy_outputs"), signals))
# num_easy_digits = 0

# Result
print(num_easy_digits)