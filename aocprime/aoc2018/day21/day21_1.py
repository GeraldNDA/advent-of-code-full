#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

from op_code import OpCode
from collections import defaultdict

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

REGISTER_ZERO_START = 0


# Actual Code
print("STARTING")
registers = [0] * REGISTER_COUNT
reg2_values = defaultdict(set)
while registers[ip_reg] < len(instructions):
    instr = instructions[registers[ip_reg]]
    if instr == ("eqrr",2, 0, 3):
        if tuple(registers) in reg2_values[registers[2]]:
            break
        reg2_values[registers[2]].add(tuple(registers))
        print(registers[2], registers[0])
    # if instr == ("gtrr",1, 5, 1):
    #     print(registers[1], registers[5])
    OpCode.perform_op(*instr, registers=registers)
    registers[ip_reg] += 1
 

# Result
print()
print(registers[0])