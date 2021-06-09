#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller
# Input Parse
puzzle = AdventOfCode(year=2020, day=4)
puzzle_input = puzzle.get_input()

# Oarse frin strean
class Passport:
    REQUIRED_FIELDS = {
        "byr", "iyr", "eyr",
        "hgt", "hcl", "ecl",
        "pid", 
        # "cid",
    }

    def __init__(self, data) -> None:
        self.data = data

    def is_valid(self):
        return not (Passport.REQUIRED_FIELDS - set(self.data.keys()))

    @staticmethod
    def from_stream(stream):
        data = {}
        for line in stream:
            if not line:
                break
            data.update(map(methodcaller("split", ":"), line.split(" ")))
        return Passport(data) if data else None

    def __repr__(self) -> str:
        return f"Passport({str(self.data)})"

passport_info = iter(puzzle_input)
passports = []

passport = Passport.from_stream(passport_info)
while passport:
    passports.append(passport)
    passport = Passport.from_stream(passport_info)

# Actual Code
valid_passports = len(list(filter(methodcaller("is_valid"), passports)))


# Result
print(valid_passports)