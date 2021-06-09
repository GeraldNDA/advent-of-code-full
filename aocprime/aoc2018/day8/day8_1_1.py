#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=8)
puzzle_input = puzzle.get_input()

tree_info = list(map(int, puzzle_input.split(" ")))

def get_next_info():
    return tree_info.pop(0)

class TreeNode:
    def __init__(self, children=None, metadata=None):
        self.children = children if children is not None else set()
        self.metadata = metadata if metadata is not None else set()
    def __add__(self, other):
        if type(other) is int:
            return self.sum_all() + other
        elif isinstance(other, TreeNode):
            return self.sum_all() + other.sum_all()
        else:
            raise NotImplementedError
    
    def __radd__(self, other):
        return self + other

    def sum_all(self):
        return sum(self.children) + sum(self.metadata)

def replicateParser(amount, parser):
    def parser(value):
        value = value[:]
        for i in range(amount):
            parser(value.pop(0))
    return parser


def get_tree(value):
    value = value[:]
    num_children = value.pop(0)
    num_metadata = value.pop(0)
    return TreeNode(
        children=replicateParser(num_children, get_tree)(value),
        metadata=replicateParser(num_metadata, lambda x: x.pop(0) )(value)
    )
tree = get_tree(tree_info)
print( tree.sum_all() )