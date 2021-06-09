# Imports
from copy import deepcopy
from collections import defaultdict

# File IO
with open('day25.txt', 'r') as f:
  inpt = f.read().splitlines()
# Input Parsing
states = {}
start = "A"
checksum = 0

state = None
curr_state = None
curr_value = None
in_state = False
i = 0
while i < len(inpt):
  line = inpt[i].strip().split(" ")
  if line[0] == "Begin":
    start = line[-1].strip(".")
  elif "checksum" in line:
    checksum = int(line[-2])
  elif not line or not line[0]:
    if curr_state:
      states[state] = deepcopy(curr_state)
    
    state = None
    in_state = False
    curr_state = None
    curr_value = None
  elif line[0] == "In":
    state = line[-1].strip(":")
    curr_state = {}
  elif line[0] == "If":
    curr_value = int(line[-1].strip(":"))
    curr_state[curr_value] = {}
  elif line[0] == "-":
    if line[1] == "Write":
      curr_state[curr_value]["w"] = int(line[-1].strip("."))
    elif line[1] == "Move":
      curr_state[curr_value]["m"] = line[-1].strip(".")[0]
    elif line[1] == "Continue":
      curr_state[curr_value]["n"] = line[-1].strip(".")
  i += 1

# Run program
cursor = 0
state = start
tape = defaultdict(lambda: 0)
for i in xrange(checksum):
  instructions = states[state][tape[cursor]]
  tape[cursor] = instructions["w"]
  if instructions["m"] == "r":
    cursor += 1
  else:
    cursor -= 1
  state = instructions["n"]

# Result Parsing
print sum(tape.values())