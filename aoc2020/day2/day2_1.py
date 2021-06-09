#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller

# Input Parse
puzzle = AdventOfCode(year=2020, day=2)
puzzle_input = puzzle.get_input()

class PasswordPolicy:
    def __init__(self, start, stop, letter):
        self.start = start
        self.stop = stop
        self.letter = letter

    @staticmethod
    def from_stream(char_stream):
        range_string = ""
        letter = ""
        for char in char_stream:
            if char == " ":
                break
            range_string += char
        for char in char_stream:
            if char == ":":
                break
            letter += char
        return PasswordPolicy(*map(int, range_string.split("-")), letter)

    def pass_is_valid(self, password):
        return password.count(self.letter) in range(self.start, self.stop + 1)

    def __repr__(self) -> str:
        return f"PassPolicy({self.start}, {self.stop}, {self.char})"

class PasswordEntry:
    def __init__(self, policy, password):
        self.policy = policy
        self.password = password
    
    @staticmethod
    def from_line(line):
        stream = iter(line)
        return PasswordEntry(PasswordPolicy.from_stream(stream), "".join(stream).strip())

    def is_valid(self):
        return self.policy.pass_is_valid(self.password)

    def __repr__(self) -> str:
        return f"PassEntry({self.policy}, {self.password})"

# Actual Code
valid_passwords = len(list(filter(methodcaller("is_valid"), map(PasswordEntry.from_line, puzzle_input))))
# Result
print(valid_passwords)