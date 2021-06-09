# Better solution because it works with part 2 ...
# Imports

# File IO
data_pos = 347991
# Actual Code

dirs = {
  "right": (1, 0),  
  "left": (-1, 0),
  "up": (0, -1),
  "down": (0, 1)
}

steps = ["right","down", "left", "up"]
curr_step = 0


positions = {(0,0): 1}

curr_n = 1
width = 1
count = 0
curr_pos = [0,0]
  
while curr_n < data_pos:
  
  for i in range(width):
    curr_pos[0] += dirs[steps[curr_step]][0]
    curr_pos[1] += dirs[steps[curr_step]][1]
    curr_n += 1
    positions[tuple(curr_pos)] = curr_n
    if curr_n == data_pos:
      break
     
  if curr_n != data_pos:
    if count < 1:
      count += 1
    else:
      width += 1
      count = 0
   
    curr_step = (curr_step + 1 ) % 4
print sum(map(abs, curr_pos))