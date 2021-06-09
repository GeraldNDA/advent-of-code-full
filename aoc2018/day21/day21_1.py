#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from op_code import OpCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=21)
puzzle_input = puzzle.get_input()

# Actual Code
result = puzzle_input
REGISTER_COUNT = 6

instruction_pointer_line = puzzle_input.pop(0)
ip_reg = int(instruction_pointer_line.split(" ")[-1])
instructions = [

]
for line in puzzle_input:
    line = line.split(" ")
    line[1:] = tuple(map(int, line[1:]))
    instructions.append(tuple(line))

REGISTER_ZERO_START = 500


# Actual Code
for reg_0 in reversed(range(REGISTER_ZERO_START)):
    registers = [0] * REGISTER_COUNT
    registers[0] = reg_0
    instructions_run = 0
    while registers[ip_reg] < len(instructions):
        instr = instructions[registers[ip_reg]]
        OpCode.perform_op(*instr, registers=registers)
        registers[ip_reg] += 1
        instructions_run += 1
    print(reg_0, instructions_run)
 

# Result
print()
print(registers[0])