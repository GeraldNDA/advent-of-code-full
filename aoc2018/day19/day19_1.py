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

# Actual Code
while registers[ip_reg] < len(instructions):
    instr = instructions[registers[ip_reg]]
    OpCode.perform_op(*instr, registers=registers)
    registers[ip_reg] += 1
    print(registers[ip_reg], registers, end=" " *30 + "\r")


# Result
print()
print(registers[0])