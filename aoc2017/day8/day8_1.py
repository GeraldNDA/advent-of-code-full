# Imports
from collections import defaultdict

# File IO
with open('day8.txt', 'r') as f:
  inpt = f.read().splitlines()

# Actual Code
registers = defaultdict(lambda: 0)
for line in inpt:
  line = line.split(" ")
  register = line[0]
  op = line[1]
  value = int(line[2])
  
  compare_reg = line[4]
  check = " ".join(line[5:])
  if eval("registers['" +compare_reg +"'] " + check):
    if op == "dec":
     registers[register] -= value
    elif op == "inc":
      registers[register] += value

# Result Parsing
print max(registers.values())