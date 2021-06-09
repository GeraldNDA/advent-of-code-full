#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from functools import reduce
from operator import and_, methodcaller
# Input Parse
puzzle = AdventOfCode(year=2020, day=6)
puzzle_input = puzzle.get_input()

class AnswerGroup:
    def __init__(self, answers) -> None:
        self.answers = answers

    @staticmethod
    def from_stream(stream):
        answers = []
        for line in stream:
            if not line:
                break
            answers.append(line)
        return AnswerGroup(answers) if answers else None

    def questions(self):
        return reduce(and_, map(set, self.answers))


# Actual Code
responses = iter(puzzle_input)
answer_groups = []

answer_group = AnswerGroup.from_stream(responses)
while answer_group:
    answer_groups.append(answer_group)
    answer_group = AnswerGroup.from_stream(responses)

num_questions = sum(map(len, map(methodcaller("questions"), answer_groups)))

# Result
print(num_questions)