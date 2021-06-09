#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=14)
puzzle_input = puzzle.get_input()
puzzle_input = "880751"

sequence = tuple(map(int, puzzle_input))
sequence_len = len(sequence)
# Actual Code
scoreboard = [3, 7]
len_scoreboard = 2
last_slice = scoreboard[:]
elf_1 = 0
elf_2 = 1
done = False
amount_before = 0
# itr_count = 0
while True:
    # print(itr_count, end="\r")
    # itr_count += 1
    recipe_score = scoreboard[elf_1] + scoreboard[elf_2]
    score_digits = tuple(map(int, str(recipe_score)))
    
    scoreboard.extend(score_digits)
    len_scoreboard += len(score_digits)

    last_slice.extend(score_digits)
    last_slice = last_slice[-sequence_len-1:]
    if len(last_slice) == sequence_len + 1:
        if tuple(last_slice[1:]) == sequence:
            amount_before = len_scoreboard - sequence_len
            break
        elif tuple(last_slice[:-1]) == sequence:
            amount_before = len_scoreboard - sequence_len - 1
            break

    elf_1 = (elf_1 + 1 + scoreboard[elf_1]) % len_scoreboard
    elf_2 = (elf_2 + 1 + scoreboard[elf_2]) % len_scoreboard
# Result
print(amount_before)