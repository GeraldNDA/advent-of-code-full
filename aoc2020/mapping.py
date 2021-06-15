
import operator
from enum import Enum
from typing import NamedTuple
from itertools import starmap

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(*starmap(operator.add, zip(self, other)))
        if isinstance(other, int):
            return Point(self.x + other, self.y + other)
        return NotImplemented
   
    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(*starmap(operator.mul, zip(self, other)))
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return Point(*map(operator.neg, self))

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

class CardinalDirections(Enum):
    NORTH = Point(0, -1)
    EAST = Point(+1, 0)
    SOUTH = Point(0, +1)
    WEST = Point(-1, 0)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

class OrdinalDirections(Enum):
    NORTH = CardinalDirections.NORTH.value
    NORTH_EAST = CardinalDirections.NORTH.value + CardinalDirections.EAST.value
    EAST = CardinalDirections.EAST.value
    SOUTH_EAST = CardinalDirections.SOUTH.value + CardinalDirections.EAST.value
    SOUTH = CardinalDirections.SOUTH.value
    SOUTH_WEST = CardinalDirections.SOUTH.value + CardinalDirections.WEST.value
    WEST = CardinalDirections.WEST.value
    NORTH_WEST = CardinalDirections.NORTH.value + CardinalDirections.WEST.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value
