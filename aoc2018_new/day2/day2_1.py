#!/usr/bin/env python3
# Imports

# File IO
with open('day2.txt', 'r') as f:
  box_ids = f.read().splitlines()

# Actual Code
two_letter = 0
three_letter = 0
for box_id in box_ids:
  if set(filter(lambda l: box_id.count(l) == 2, set(box_id))):
    two_letter += 1
  if set(filter(lambda l: box_id.count(l) == 3, set(box_id))):
    three_letter += 1

# Result Parsing
print("checksum:", two_letter * three_letter)