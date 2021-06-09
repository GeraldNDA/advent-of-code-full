#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

import re
import sys

from subprocess import check_output
from time import sleep

# Input Parse
puzzle = AdventOfCode(year=2018, day=10)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "position=< 9,  1> velocity=< 0,  2>",
#     "position=< 7,  0> velocity=<-1,  0>",
#     "position=< 3, -2> velocity=<-1,  1>",
#     "position=< 6, 10> velocity=<-2, -1>",
#     "position=< 2, -4> velocity=< 2,  2>",
#     "position=<-6, 10> velocity=< 2, -2>",
#     "position=< 1,  8> velocity=< 1, -1>",
#     "position=< 1,  7> velocity=< 1,  0>",
#     "position=<-3, 11> velocity=< 1, -2>",
#     "position=< 7,  6> velocity=<-1, -1>",
#     "position=<-2,  3> velocity=< 1,  0>",
#     "position=<-4,  3> velocity=< 2,  0>",
#     "position=<10, -3> velocity=<-1,  1>",
#     "position=< 5, 11> velocity=< 1, -2>",
#     "position=< 4,  7> velocity=< 0, -1>",
#     "position=< 8, -2> velocity=< 0,  1>",
#     "position=<15,  0> velocity=<-2,  0>",
#     "position=< 1,  6> velocity=< 1,  0>",
#     "position=< 8,  9> velocity=< 0, -1>",
#     "position=< 3,  3> velocity=<-1,  1>",
#     "position=< 0,  5> velocity=< 0, -1>",
#     "position=<-2,  2> velocity=< 2,  0>",
#     "position=< 5, -2> velocity=< 1,  2>",
#     "position=< 1,  4> velocity=< 2,  1>",
#     "position=<-2,  7> velocity=< 2, -2>",
#     "position=< 3,  6> velocity=<-1, -1>",
#     "position=< 5,  0> velocity=< 1,  0>",
#     "position=<-6,  0> velocity=< 2,  0>",
#     "position=< 5,  9> velocity=< 1, -2>",
#     "position=<14,  7> velocity=<-2,  0>",
#     "position=<-3,  6> velocity=< 2, -1>"
# ]

class Point():
    POINT_INFO_LINE_MATCHER = re.compile(r"position=<\s*(-?\d+)\s*,\s*(-?\d+)\s*> velocity=<\s*(-?\d+)\s*,\s*(-?\d+)\s*>")
    def __init__(self, position=(0,0), velocity=(0,0)):
        self.position = position
        self.velocity = velocity
    
    def move(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        )
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(
                position=(self.position[0] + other.position[0], self.position[1] + other.position[1]), 
                velocity=(self.velocity[0] + other.velocity[0], self.velocity[1] + other.velocity[1]), 
            )
        raise NotImplementedError

    def __repr__(self):
        return f"Point(position={self.position}, velocity={self.velocity})"

    @staticmethod
    def parse_point_info(point_info):
        point_info = Point.POINT_INFO_LINE_MATCHER.match(point_info)
        if not point_info:
            raise ValueError
        else:
            point_info = point_info.groups()
            return Point(tuple(map(int, point_info[0:2])), tuple(map(int, point_info[2:4])))

    @staticmethod
    def make_dir_set(position):
        return (
            (position[0] + 1, position[1]),
            (position[0] - 1, position[1]),
            (position[0], position[1] + 1),
            (position[0], position[1] - 1)
        )
class Sky():
    def __init__(self, points, display_width=None, display_height=None, top_left=(-10, -10)):
        self.points = points
        if display_width is None or display_height is None:
            rows, columns = check_output(['stty', 'size']).split()
            self.display_width = int(columns)-1 if display_width is None else display_width
            self.display_height = int(rows)-1 if display_height is None else display_height
        self.clear()
        self.top_left = (-10, -10)
        self.bottom_right = (
            self.top_left[0] + self.display_width,
            self.top_left[1] + self.display_height,
        )

    def clear(self):
        self.grid = []
        for _ in range(self.display_height):
            self.grid.append(["." for x in range(self.display_width)] )
        print("\033c")

    def increment(self):
        for point in self.points:
            point.move()
    
    def all_beside(self):
        pos_set = set(p.position for p in self.points)
        for pos in pos_set:
            if not any(map(lambda p: p in pos_set, Point.make_dir_set(pos))):
                return False
        return True

    def center_display(self):
        avg_point = sum(self.points, Point())
        avg_point.position = (
            avg_point.position[0] // len(self.points),
            avg_point.position[1] // len(self.points),
        )
        # shift it to top left
        avg_point.velocity = (
            -1*self.display_width // 2,
            -1*self.display_height // 2
        )
        avg_point.move()
        self.top_left = tuple(avg_point.position)
        avg_point.velocity = (
            self.display_width,
            self.display_height,
        )
        avg_point.move()
        self.bottom_right = tuple(avg_point.position)

    def display(self):
        self.clear()
        for point in self.points:
            if self.top_left[0] <= point.position[0] < self.bottom_right[0]:
                if self.top_left[1] <= point.position[1] < self.bottom_right[1]:
                    (x, y) = (
                        point.position[0] - self.top_left[0],
                        point.position[1] - self.top_left[1]
                    )
                    self.grid[y][x] = "#"
        print("\n".join(map(lambda line: "".join(line), self.grid)))


point_info = list(map(Point.parse_point_info, puzzle_input))
my_sky = Sky(point_info)

while True:
    my_sky.increment()
    if my_sky.all_beside():
        break

my_sky.center_display()
my_sky.display()