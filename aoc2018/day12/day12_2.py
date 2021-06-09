#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=12)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "initial state: #..#.#..##......###...###",
#     "",
#     "...## => #",
#     "..#.. => #",
#     ".#... => #",
#     ".#.#. => #",
#     ".#.## => #",
#     ".##.. => #",
#     ".#### => #",
#     "#.#.# => #",
#     "#.### => #",
#     "##.#. => #",
#     "##.## => #",
#     "###.. => #",
#     "###.# => #",
#     "####. => #"
# ]

def parse_information(puzzle_input):
    initial_state = None
    rules = []
    for line in puzzle_input:
        if line.startswith("initial state:"):
            initial_state = line[len("initial state: "):]
        elif line.strip():
            rules.append(tuple(line.split(" => ")))
    return initial_state, dict(rules)
garden, rules = parse_information(puzzle_input)
max_generation = 50_000_000_000
# Actual Code
#..#.#..##......###.. .###
start_index = 0
seen = {}
for generation in range(max_generation):
    seen[garden] = (generation, start_index)
    garden = "...." + garden + "...."
    start_index -= 4
    next_generation = list(garden)
    for pot in range(len(garden) - 4):
        affected_pot = pot + 2
        pot_group = garden[pot:pot + 5]
        if pot_group in rules:
            next_generation[affected_pot] = rules[pot_group]
        else:
            next_generation[affected_pot] = "."
    starting_dots = 0
    while next_generation[starting_dots] == ".":
        starting_dots += 1
    start_index += starting_dots
    garden = "".join(next_generation).strip(".")

    if garden in seen:
        curr_generation, curr_start = generation + 1, start_index
        prev_generation, prev_start = seen[garden]
        
        generations_to_go = max_generation - curr_generation
        index_diff = (curr_start - prev_start) // (curr_generation - prev_generation)
        start_index += index_diff * generations_to_go
        break

# Result
print(sum(i for i in range(start_index, start_index+len(garden)) if garden[i - start_index] == "#"))