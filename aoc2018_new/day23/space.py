#!/usr/bin/env python3
from typing import NamedTuple
from typing import Tuple, Optional
from itertools import product
from math import sqrt

class Bounds(NamedTuple):
    # Includes both lower and upperbound
    lower_bound:int
    upper_bound:int

    def midpoint(self):
        return max((self.lower_bound + self.upper_bound)//2, self.lower_bound)

    def split(self, mid:int=None):
        if mid is None:
            mid = self.midpoint()
        lower_bound, upper_bound = self
        if upper_bound == lower_bound:
            return (self, self)
        assert mid < upper_bound
        return (Bounds(lower_bound, mid), Bounds(mid+1, upper_bound))

    def clamp(self, x:int) -> int:
        lower_bound, upper_bound = self
        return max(lower_bound, min(x, upper_bound))

    def merge(self, other:"Bounds") -> "Bounds":
        return Bounds(min(self.lower_bound, other.lower_bound), max(self.upper_bound, other.upper_bound))

    def has(self, x:int) -> bool:
        return self.lower_bound <= x <= self.upper_bound

class ManhattanSphere:
    centre: Tuple[int, int, int]
    radius: int

    def __init__(self, centre:Tuple[int, int, int], radius:int):
        self.centre = centre
        self.radius = radius

class SignalSpace:
    edges:Tuple[Bounds, Bounds, Bounds]
    
    def __init__(self, edges: Tuple[Bounds, Bounds, Bounds]):
        self.edges = edges

    def split(self, midpoints:Tuple[int, int, int]=(None, None, None)):
        possible_bounds = [edge.split(midpoint) for edge, midpoint in zip(self.edges, midpoints)]
        for new_edges in product(*possible_bounds):
            yield type(self)(tuple(new_edges))

    def merge(self, other:Optional["SignalSpace"]) -> "SignalSpace":
        if other is None:
            return self
        return type(self)(tuple([edge.merge(other_edge) for edge, other_edge in zip(self.edges, other.edges)]))

    def distance(self, point: Tuple[int, int, int]) -> int:
        distance = 0
        for dim, edge in zip(point, self.edges):
            distance += max(edge.lower_bound - dim, 0, dim - edge.upper_bound)**2
        return sqrt(distance)

    def contains(self, sphere:ManhattanSphere) -> bool:
        return self.distance(sphere.centre) <= sphere.radius

    def slice(self, dim:int, centre:int):
        top = None
        bottom = None
        if not self.edges[dim].has(centre):
            raise ValueError(f"Can't slice {self.edges[dim]} using {centre} because it is not within bounds")
        if centre != self.edges[dim].upper_bound:
            new_bounds = list(self.edges)
            new_bounds[dim] = Bounds(self.edges[dim].lower_bound, centre)
            top = type(self)(tuple(new_bounds))
            new_bounds[dim] = Bounds(centre+1,self.edges[dim].upper_bound)
            return top, type(self)(tuple(new_bounds))
        elif centre != self.edges[dim].upper_bound:
            new_bounds = list(self.edges)
            new_bounds[dim] = Bounds(self.edges[dim].lower_bound, centre-1)
            top = type(self)(tuple(new_bounds))
            new_bounds[dim] = Bounds(centre,self.edges[dim].upper_bound)
            return top, type(self)(tuple(new_bounds))
        else:
            return self, self
            
    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, type(self)):
            return all(own_edge == other_edge for  own_edge, other_edge in zip(self.edges, other.edges))

