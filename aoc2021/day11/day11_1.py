#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
# Imports
from aoc import AdventOfCode

from itertools import product
from typing import NamedTuple

# Input Parse
puzzle = AdventOfCode(year=2021, day=11)
puzzle_input = puzzle.get_input()



class GridPos(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return GridPos(*map(sum, zip(self, other)))

DIRECTIONS = set(GridPos(*direction) for direction in product((-1, 0, 1), repeat=2) if direction != (0, 0))

class Octopus:
    def __init__(self, pos, initial_energy_level) -> None:
        self.pos = pos
        self.energy_level = initial_energy_level
        self.flashing = False
        self.neighbours = set()

    def set_neighbours(self, neighbours):
        self.neighbours = set(neighbours)

    def increase_energy(self):
        if not (self.energy_level == 0 and self.flashing):
            self.energy_level = (self.energy_level + 1) % 10
            if self.energy_level == 0:
                self.flashing = True
                for n in self.neighbours:
                    n.increase_energy()

    def step(self):
        self.increase_energy()

    def reset_step(self):
        flashed, self.flashing = self.flashing, False
        return flashed


# Actual Code
octopus_map = {}
for r, row in enumerate(puzzle_input):
    for c, energy_level in enumerate(row):
        octopus_map[GridPos(r, c)] = Octopus(GridPos(r, c), int(energy_level))

for pos, octopus in octopus_map.items():
    octopus.set_neighbours(octopus_map[pos+d] for d in DIRECTIONS if pos+d in octopus_map)

flash_count = 0
for step in range(100):
    for octopus in octopus_map.values():
        octopus.step()
    for octopus in octopus_map.values():
        flash_count += octopus.reset_step()

    print(f"After step {step+1}")
    for r, row in enumerate(puzzle_input):
        for c, _ in enumerate(row):
            print(octopus_map[GridPos(r, c)].energy_level, end="")
        print()

# Result
print(flash_count)