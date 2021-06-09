#!/usr/bin/env python3
# Imports
from itertools import combinations
# File IO
with open('day2.txt', 'r') as f:
  box_ids = f.read().splitlines()

# Actual Code
two_letter = 0
three_letter = 0
for box_id1, box_id2 in combinations(box_ids, 2):
  common = ""
  diff = 0
  for idx, letter in enumerate(box_id1):
    if box_id2[idx] == letter:
      common += letter
    else:
      diff += 1
      if diff > 1:
        break
  if diff == 1:
    print(common)
    break