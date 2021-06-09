# Imports
import itertools
# File IO
data_pos = 347991
# Actual Code
every_dir = list(itertools.product((1,0,-1), repeat=2))
del every_dir[every_dir.index((0,0))]

dirs = {
  "right": (1, 0),  
  "left": (-1, 0),
  "up": (0, -1),
  "down": (0, 1)
}

steps = ["right","down", "left", "up"]
curr_step = 0


positions = {(0,0): 1}
def add_adjacent_positions(current_position, positions):
  sum = 0
  for dir in every_dir:
    new_pos = (current_position[0] + dir[0], current_position[1] + dir[1])
    if new_pos in positions:
      sum += positions[new_pos]
  return sum

curr_n = 1
width = 1
count = 0
curr_pos = [0,0]
  
while curr_n < data_pos:
  
  for i in range(width):
    curr_pos[0] += dirs[steps[curr_step]][0]
    curr_pos[1] += dirs[steps[curr_step]][1]
    curr_n = add_adjacent_positions(curr_pos, positions)
    positions[tuple(curr_pos)] = curr_n
    if curr_n >= data_pos:
      break
  if curr_n < data_pos:
    if count < 1:
      count += 1
    else:
      width += 1
      count = 0
   
    curr_step = (curr_step + 1 ) % 4
print curr_n