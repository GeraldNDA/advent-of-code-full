#!/usr/bin/env python3
# Imports
import sys
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
check_line = 0
for idx, line in enumerate(puzzle_input):
    line = line.split(" ")
    line[1:] = tuple(map(int, line[1:]))
    if line == ["eqrr",2, 0, 3]:
        check_line = idx
    instructions.append(OpCode.get_op(*line))

REGISTER_ZERO_START = 0


# Actual Code
# Executing pure functions is not much faster than translated assembly
# Should probably look into which translated constructs saved the most time ... (like if statements) 
print("STARTING")
registers = [0] * REGISTER_COUNT
reg2_values = set()
last_val = None
i = 1
while registers[ip_reg] < len(instructions):
    if registers[ip_reg] == check_line:
        if registers[2] in reg2_values:
            break
        reg2_values.add(registers[2])
        last_val = registers[2]
        i += 1
        print(i, " "*20, end="\r")
    instr = instructions[registers[ip_reg]]
    instr(registers)
    registers[ip_reg] += 1

# Result
print("SOLUTION", last_val)
sys.exit(0)


# Manually translated input "assembly" to python to decrease runtime
import translated_input
# Result
print(translated_input.solver())