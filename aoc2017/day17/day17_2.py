# Imports

# File IO
#with open('day17.txt', 'r') as f:
inpt = 343
# inpt = 3
  

# Actual Code
curr_pos = 1
pos1 = 1

i = 2
max_iter = int("50,000,000".translate(None, ","))
while i <= max_iter:
  curr_pos = ((curr_pos  + inpt) % i ) + 1
  if curr_pos == 1:
    pos1 = i
  i += 1
# Result Parsing
print pos1