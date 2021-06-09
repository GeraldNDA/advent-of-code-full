# Imports
import math
# File IO
with open('day11.txt', 'r') as f:
  inpt = f.read()
path = inpt.split(",")

dirs = set(["n", "ne", "nw", "se", "sw", "s"])
def sign(x):
  if not x:
    return 0
  return int(math.copysign(1,x))
# Actual Code
pos = [0,0]
# n/s = +/-
# nw/se = +/-
# ne/sw = 
for step in path:
  if step == "n":
    pos[0] += 1
  elif step == "s":
    pos[0] -= 1
  elif step == "ne":
    pos[1] += 1
  elif step == "sw":
    pos[1] -= 1
  elif step == "nw":
    pos[0] += 1
    pos[1] -= 1
  elif step == "se":
    pos[0] -= 1
    pos[1] += 1
  
# Result Parsing
result = 0
# print sign(pos[0]), -1*sign(pos[1]), sign(pos[0])
if sign(pos[0]) == -1*sign(pos[1]) and sign(pos[0]):
  abs_pos = map(abs, pos)
  result = min(abs_pos) + (max(abs_pos) - min(abs_pos))
else:
  result = sum(map(abs, pos))
print result
# n + nw
# s + se

