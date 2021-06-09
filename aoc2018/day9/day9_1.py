#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=9)
puzzle_input = puzzle.get_input()
puzzle_input = "30 players; last marble is worth 5807 points"

def parse_game_info(line):
    line = line.split(" ")
    return(int(line[0]), int(line[-2]))

(num_players, last_marble_worth) = parse_game_info(puzzle_input)

scores = [0]* num_players
marble_circle = [0]
len_marble_circle = 9
position = 0
for marble in range(1, last_marble_worth + 1):
    if marble % 23:
        position = (position + 2) % len(marble_circle)
        marble_circle.insert(position, marble)
        len_marble_circle += 1
    else:
        current_player = (marble - 1) % num_players
        position = (position - 7) % len(marble_circle)
        removed_marble = marble_circle.pop(position)
        scores[current_player] += marble + removed_marble
    print(marble, max(scores))
# Result
print()
print(max(scores))