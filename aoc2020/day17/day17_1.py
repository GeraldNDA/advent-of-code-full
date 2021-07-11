#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from collections import defaultdict
from enum import Enum
from mapping import all_directions

# Input Parse
puzzle = AdventOfCode(year=2020, day=17)
puzzle_input = puzzle.get_input()

class CubeState(Enum):
    ACTIVE = "#"
    INACTIVE = "."

    def flip(self):
        return CubeState.INACTIVE if self is CubeState.ACTIVE else CubeState.ACTIVE


class ConwayCube:
    def __init__(self, state=CubeState.INACTIVE) -> None:
        self.state = state
        self.next_state = state
        self.neighbours = set()

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_next_state(self):
        active_neighbours = sum(1 for neighbour in self.neighbours if neighbour.state is CubeState.ACTIVE)
        if self.state is CubeState.ACTIVE and active_neighbours not in (2, 3):
            self.next_state = CubeState.INACTIVE
        elif self.state is CubeState.INACTIVE and active_neighbours == 3:
            self.next_state = CubeState.ACTIVE
        else:
            self.next_state = self.state

    def tick(self):
        self.state = self.next_state

class PocketDimension:
    def __init__(self) -> None:
        self.cubes = defaultdict(ConwayCube)

    @staticmethod
    def from_map(dim_map):
        dimension = PocketDimension()
        for ridx, row in enumerate(dim_map):
            for cidx, cube_state in enumerate(row):
                pos = (ridx, cidx, 0)
                cube = dimension.cubes[pos]
                cube.state = CubeState(cube_state)
                cube.next_state = cube.state
                cube.set_neighbours(tuple(dimension.cubes[tuple(map(sum, zip(pos, direction)))] for direction in all_directions() if direction != (0,0,0)))
        return dimension

    def tick(self):
        cubes = tuple(self.cubes.items())
        for pos, cube in cubes:
            if not cube.neighbours:
                cube.set_neighbours(tuple(self.cubes[tuple(map(sum, zip(pos, direction)))] for direction in all_directions() if direction != (0,0,0)))
            cube.get_next_state()
        for _, cube in cubes:
            cube.tick()

    def boot_process(self):
        for _ in range(6):
            self.tick()

# Actual Code
dimension = PocketDimension.from_map(puzzle_input)
dimension.boot_process()


# Result
print(sum(cube.state is CubeState.ACTIVE for cube in dimension.cubes.values()))