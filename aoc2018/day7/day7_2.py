#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from collections import defaultdict, OrderedDict
# Input Parse
puzzle = AdventOfCode(year=2018, day=7)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "Step C must be finished before step A can begin.",
#     "Step C must be finished before step F can begin.",
#     "Step A must be finished before step B can begin.",
#     "Step A must be finished before step D can begin.",
#     "Step B must be finished before step E can begin.",
#     "Step D must be finished before step E can begin.",
#     "Step F must be finished before step E can begin."
# ]
num_elves = 5
min_task_time = 60
###

def parse_dependency(line):
    line = line.split()
    if line:
        return (line[1], line[-3])

step_relations = map(parse_dependency, puzzle_input)

# Actual Code
in_degree_map  = defaultdict(int)
connection_map = defaultdict(list)
dependency_map = defaultdict(list)
for step_relation in step_relations:
    in_degree_map[step_relation[1]] += 1
    in_degree_map[step_relation[0]] += 0
    connection_map[step_relation[0]].append(step_relation[1])
    dependency_map[step_relation[1]].append(step_relation[0])

in_degree_map = OrderedDict(sorted(in_degree_map.items()))

task_to_time = lambda t: ord(t) - ord("A") + 1
elf_tasks = [None] * num_elves
tick = -1

def do_elf_tasks():
    global tick
    tick += 1
    # print(elf_tasks,  end="\r\n")
    for i, task in enumerate(elf_tasks):
        if task is not None:
            task[-1] -= 1
            if task[-1] == 0:
                elf_tasks[i] = None

def being_done(t):
    return any(map(lambda et: et and t == et[0], elf_tasks))
while in_degree_map:
    # decrement all
    do_elf_tasks()
    while None in elf_tasks and in_degree_map:
        min_in_deg = None
        for task, in_degree in in_degree_map.items():
            if in_degree != 0:
                continue
            if not any(map(lambda d: being_done(d),  dependency_map[task])):
                min_in_deg = task
                break
        
        if min_in_deg is None:
            break
        
        elf = elf_tasks.index(None)

        in_degree = in_degree_map.pop(min_in_deg)

        elf_tasks[elf] = [min_in_deg, min_task_time + task_to_time(min_in_deg)]
        # print(dependency_map[min_in_deg], elf_tasks, "\r")
        for item in connection_map[min_in_deg]:
            in_degree_map[item] -= 1

while any(elf_tasks):
    do_elf_tasks()
# Result
print(tick)