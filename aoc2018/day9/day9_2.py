#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=9)
puzzle_input = puzzle.get_input()
# puzzle_input = "9 players; last marble is worth 25 points"

def parse_game_info(line):
    line = line.split(" ")
    return(int(line[0]), int(line[-2]))

(num_players, last_marble_worth) = parse_game_info(puzzle_input)
last_marble_worth *= 100

scores = [0]* num_players
marble_circle = [0]
len_marble_circle = 1
position = 0
for marble in range(1, last_marble_worth + 1):
    if marble % 23:
        position = (position + 2) % len_marble_circle
        marble_circle.insert(position, marble) # O(m)
        len_marble_circle += 1
    else:
        current_player = (marble - 1) % num_players
        position = (position - 7) % len_marble_circle
        removed_marble = marble_circle.pop(position) # O(m)
        len_marble_circle -= 1
        scores[current_player] += marble + removed_marble
        print(marble,"=",last_marble_worth, end="\r")
# This works but is very very slow. O(m^2) should figure out how to calculate the it or remove the need to insert to arbitrary places.
# Result
print()
#print(marble_circle)
print(max(scores))