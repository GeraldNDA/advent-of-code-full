#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=14)
puzzle_input = puzzle.get_input()
recipes_to_try = int(puzzle_input)
# Actual Code
scoreboard = [3, 7]
elf_1 = 0
elf_2 = 1
while len(scoreboard) < recipes_to_try + 10:
    recipe_score = scoreboard[elf_1] + scoreboard[elf_2]
    scoreboard.extend(
        tuple(map(int, str(recipe_score)))
    )
    elf_1 = (elf_1 + 1 + scoreboard[elf_1]) % len(scoreboard)
    elf_2 = (elf_2 + 1 + scoreboard[elf_2]) % len(scoreboard)
# Result
print("".join(map(str, scoreboard[recipes_to_try:recipes_to_try+10])))