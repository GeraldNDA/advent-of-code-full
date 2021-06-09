#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from op_code import OpCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=19)
puzzle_input = puzzle.get_input()
REGISTER_COUNT = 6

registers = [0] * REGISTER_COUNT
registers[0] = 1
instruction_pointer_line = puzzle_input.pop(0)
ip_reg = int(instruction_pointer_line.split(" ")[-1])
instructions = [

]
for line in puzzle_input:
    line = line.split(" ")
    line[1:] = tuple(map(int, line[1:]))
    instructions.append(tuple(line))

register_tracker = []
ip_tracker = ""
def found_cycle(tracker):
    if not tracker:
        return False, None
    tracker_list = tracker.split(" ")
    last_value = tracker_list[-1]
    start_of_last = -len(last_value)-1
    if last_value in  tracker_list[:-1]:
        pattern = tracker[tracker[:start_of_last].rindex(last_value):start_of_last]
        if len(pattern.split(" ")) > 1 and tracker.endswith(" ".join(pattern.split(" ")*2 + [last_value])):
            return len(tracker_list) - 2 - tracker[tracker[:start_of_last].rindex(last_value):start_of_last].count(" "), pattern.split(" ")
    return False, None

# Actual Code
while registers[ip_reg] < len(instructions):
    if registers[ip_reg] == 1:
            print("Reached two():", registers)
            break
    
    while not found_cycle(ip_tracker)[0] and registers[ip_reg] < len(instructions):
        ip_tracker += " " + str(registers[ip_reg])
        ip_tracker = ip_tracker.strip()
        register_tracker.append(tuple(registers))
        instr = instructions[registers[ip_reg]]
        OpCode.perform_op(*instr, registers=registers)
        registers[ip_reg] += 1
        if registers[ip_reg] == 1:
            print("Reached two():", registers)
            break
    if registers[ip_reg] == 1:
        break
    last_index, pattern = found_cycle(ip_tracker)
    if not pattern:
        break
    last_register_values = register_tracker[last_index]
    register_diff = tuple(map(
        lambda i: registers[i] - last_register_values[i],
        range(len(registers))
    ))
    end_of_compute = 0
    instructions_to_do = tuple(map(int, pattern))
    for idx, i in enumerate(map(lambda i: instructions[i], instructions_to_do)):
        end_of_compute = idx
        if i[0].startswith("gt"):
            break
    while registers[ip_reg] in instructions_to_do:
        registers = list(map(
            lambda i: registers[i] + register_diff[i],
            range(len(registers))
        ))
        for _ in range(end_of_compute, len(pattern)):
            instr = instructions[registers[ip_reg]]
            OpCode.perform_op(*instr, registers=registers)
            registers[ip_reg] += 1

    print(registers, register_diff, end="\r")
def quick_factors(n, start=1):
    factors = []
    for i in range(start, n+1):
        if n % i == 0:
            print(n,"/", i, "=>", n//i)
            factors.append(i)
    return factors
# Result
print()
# print(registers[0])
print(sum(quick_factors(registers[3])))
