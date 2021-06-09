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

curr_loop = 0
max_n = 1

while max_n < data_pos:
  max_n += 4*curr_loop
  curr_loop += 2

last_pos = [(curr_loop/2) - 1]*2
curr_n = max_n
step_count = 0
curr_pos = list(last_pos)

width = curr_loop - 2
while data_pos < curr_n:
    if step_count > width - 1:
      curr_step += 1
      step_count = 0
    curr_step = curr_step % 4
    
    curr_pos[0] -= dirs[steps[curr_step]][0]
    curr_pos[1] -= dirs[steps[curr_step]][1]
    curr_n -= 1
    step_count += 1
print curr_pos, sum(map(abs, curr_pos))