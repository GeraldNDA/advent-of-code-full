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
    FIELD_CHECKS = {
        "byr": lambda byr: byr.isdigit() and int(byr) in range(1920, 2003),
        "iyr": lambda iyr: iyr.isdigit() and int(iyr) in range(2010, 2021),
        "eyr": lambda eyr: eyr.isdigit() and int(eyr) in range(2020, 2031),
        "hgt": lambda hgt: hgt[:-2].isdigit() and (
            (hgt.endswith("cm") and int(hgt[:-2]) in range(150, 194)) or 
            (hgt.endswith("in") and int(hgt[:-2]) in range(59, 77))
        ),
        "hcl": lambda hcl: len(hcl) == 7 and hcl.startswith("#") and all((char in "0123456789abcdef") for char in hcl[1:]),
        "ecl": lambda ecl: ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth",},
        "pid": lambda pid: len(pid) == 9 and pid.isdigit(), 
        # "cid",
    }

    def __init__(self, data) -> None:
        self.data = data

    def is_valid(self):
        return all((key in self.data and val(self.data[key])) for key, val in Passport.FIELD_CHECKS.items())

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