#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

import operator
from itertools import chain

# Input Parse
puzzle = AdventOfCode(year=2020, day=18)
puzzle_input = puzzle.get_input()
# puzzle_input = ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]

# Actual Code
class Stream:
    def __init__(self, gen) -> None:
        self.gen = (_ for _ in gen)
    
    def _unpeek(self, val):
        self.gen = chain((val), self.gen)

    def try_consume(self, value):
        try:
            self.consume(value)
            return True
        except ValueError as e:
            saw = e.args[0]
            if saw is not None:
                self._unpeek(saw)
            return False

    def consume(self, value):
        val = None
        for val in self.gen:
            break
        if val != value:
            raise ValueError(val)

    def consume_digit(self):
        val = None
        for val in self.gen:
            break
        if not val.isdigit():
            raise ValueError(val)
        return int(val)

    def consume_end(self):
        remaining = tuple(self.gen)
        assert not remaining, remaining

class Terminal:
    def __init__(self, value) -> None:
        self.value = value

    def eval(self):
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"
    
    @staticmethod
    def parse(stream):
        if stream.try_consume("("):
            val = Multiplication.parse(stream)
            stream.consume(")")
            return val
        return Terminal(stream.consume_digit())

class Operation:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
        self.op = None

    def eval(self):
        return self.op(self.left.eval(), self.right.eval())

class Addition(Operation):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)
        self.op = operator.add
    
    def __repr__(self) -> str:
        return f"({self.left} + {self.right})"

    @staticmethod
    def parse(stream):
        left = Terminal.parse(stream)
        if stream.try_consume("+"):
            return Addition(left, Addition.parse(stream))
        return left


class Multiplication(Operation):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)
        self.op = operator.mul
    
    def __repr__(self) -> str:
        return f"({self.left} * {self.right})"

    @staticmethod
    def parse(stream):
        left = Addition.parse(stream)
        if stream.try_consume("*"):
            return Multiplication(left, Multiplication.parse(stream))
        return left


def parse_expr(stream):
    val = Multiplication.parse(stream)
    stream.consume_end()
    return val

def eval_expression(expression_stream):
    expr = parse_expr(Stream(filter(lambda c: c != " ", expression_stream)))
    return expr.eval()
    

# Result
homework = ((_ for _ in expr) for expr in puzzle_input)
print(sum(map(eval_expression, homework)))