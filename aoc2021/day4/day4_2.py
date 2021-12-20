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

    def call(self, ball):
        for row_idx, row in enumerate(self.rows):
            if ball in row:
                col_idx = row.index(ball)
                self.bingo_marker[row_idx][col_idx] = True
                return all(self.bingo_marker[row_idx]) or all(r[col_idx] for r in self.bingo_marker)
        return False

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
bingo_subsystem = iter(puzzle_input[1:])
while True:
    board = Board.parse(bingo_subsystem)
    if not board:
        break
    boards.append(board)

# Result
has_bingo = [False]*len(boards)
bingo_ball_stream = iter(bingo_balls)
for ball in bingo_ball_stream:
    for board_idx, board in enumerate(boards):
        if has_bingo[board_idx]:
            continue
        has_bingo[board_idx] = board.call(ball)
    if sum(has_bingo) == len(boards) - 1:
        break

last_board = next(board for board_has_bingo, board in zip(has_bingo, boards) if not board_has_bingo)
for ball in bingo_ball_stream:
    if last_board.call(ball):
        print(last_board.score(ball))
        break
