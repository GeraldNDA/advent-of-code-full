#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from cave_conflict import *

# Input Parse
puzzle = AdventOfCode(year=2018, day=15)
# Test 1
puzzle_input = [
    "#######",
    "#.G...#",
    "#...EG#",
    "#.#.#G#",
    "#..G#E#",
    "#.....#",
    "#######",
]
# Test 2
puzzle_input = [
    "#######",
    "#G..#E#",
    "#E#E.E#",
    "#G.##.#",
    "#...#E#",
    "#...E.#",
    "#######",
]
# Test 3
puzzle_input = [
    "#######",
    "#E..EG#",
    "#.#G.E#",
    "#E.##E#",
    "#G..#.#",
    "#..E#.#",
    "#######",
]
# Test 4
puzzle_input = [
    "#######",
    "#E.G#.#",
    "#.#G..#",
    "#G.#.G#",
    "#G..#.#",
    "#...E.#",
    "#######",
]
# Test 5
puzzle_input = [
    "#######",
    "#.E...#",
    "#.#..G#",
    "#.###.#",
    "#E#G#G#",
    "#...#G#",
    "#######",
]
# Test 6
puzzle_input = [
    "#########",
    "#G......#",
    "#.E.#...#",
    "#..##..G#",
    "#...##..#",
    "#...#...#",
    "#.G...G.#",
    "#.....G.#",
    "#########",
]
puzzle_input = puzzle.get_input()
# Code
cave_map  = Map()
cave_map.set_map(puzzle_input)
print(cave_map)
outcome = cave_map.perform_combat()
# Result
print("Outcome:", outcome)