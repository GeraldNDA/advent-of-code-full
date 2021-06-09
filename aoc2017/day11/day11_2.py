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
def distance(position):
  result = 0
  if sign(position[0]) == -1*sign(position[1]) and sign(position[0]):
    abs_pos = map(abs, position)
    result = min(abs_pos) + (max(abs_pos) - min(abs_pos))
  else:
    result = sum(map(abs, position))
  return result
# Actual Code
pos = [0,0]
max_dist = 0 
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
  max_dist = max(max_dist, distance(pos))
  
  
# Result Parsing
print max_dist
# n + nw
# s + se

