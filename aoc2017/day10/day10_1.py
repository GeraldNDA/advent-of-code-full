# Imports
# File IO
with open('day10.txt', 'r') as f:
  inpt = f.read()

# Actual Code
result = 0
lst = range(256)
lengths = map(int, inpt.split(","))
curr_pos = 0
skip = 0
def reverse_range(lst, start, length):
  #pre turn
  rnge = lst[start:start+length]
  extra_distance = length - (len(lst) - start)
  if extra_distance > 0:
    rnge.extend(lst[0:extra_distance])
  for i in range(length):
    reverse_idx = length - i - 1
    i = i + start
    i = i % len(lst)
    lst[i] = rnge[reverse_idx]

for length in lengths:
  reverse_range(lst, curr_pos, length)
  curr_pos += length + skip
  curr_pos = curr_pos % len(lst)
  skip += 1

# Result Parsing
print lst[0] * lst[1]