# Imports

# File IO
#with open('day17.txt', 'r') as f:
inpt = 343
# inpt = 3
  

# Actual Code
curr_pos = 1

spin_lock = [0, 1]

i = 2
while i <= 2017:
  curr_pos = ((curr_pos  + inpt) % i ) + 1
  spin_lock = spin_lock[0:curr_pos] + [i] + spin_lock[curr_pos:]
  i += 1
# Result Parsing
print spin_lock[curr_pos],"==>", spin_lock[curr_pos + 1] 