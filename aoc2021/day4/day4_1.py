#!/usr/bin/env python3
# Add current dir to path
from itertools import chain
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2021, day=4)
puzzle_input = puzzle.get_input()

bingo_balls = tuple(map(int, puzzle_input.pop(0).split(",")))

class Board:
    def __init__(self) -> None:
        self.rows = []
        self.bingo_marker = []

    def __bool__(self):
        return bool(self.rows)

    def call_ball(self, ball):
        for row_idx, row in enumerate(self.rows):
            if ball in row:
                col_idx = row.index(ball)
                self.bingo_marker[row_idx][col_idx] = True
                return all(self.bingo_marker[row_idx]) or all(r[col_idx] for r in self.bingo_marker)

    def score(self, ball):
        return sum(num for mark, num in zip(chain(*self.bingo_marker), chain(*self.rows)) if not mark) * ball


    @staticmethod
    def parse(ball_stream):
        board = Board()
        for line in ball_stream:
            if not line:
                break
            board.rows.append(tuple(map(int, filter(None, line.split(" ")))))
        board.rows = tuple(board.rows)
        board.bingo_marker = [[False]*len(row) for row in board.rows]
        return board

# Actual Code
boards = []
bingo_subsystem = (line for line in puzzle_input[1:])
while True:
    board = Board.parse(bingo_subsystem)
    if not board:
        break
    boards.append(board)

# Result
bingo = False
for ball in bingo_balls:
    for board in boards:
        bingo = board.call_ball(ball)
        if bingo:
            print(board.score(ball))
            break
    if bingo:
        break