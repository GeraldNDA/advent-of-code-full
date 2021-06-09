#!/usr/bin/env python3
# Imports

# File IO
with open('day1.txt', 'r') as f:
  frequencies = f.readlines()

# Actual Code
reached = set() # if this is a list, it's too slow
total = 0
duplicate_found = False
while not duplicate_found:
  for frequency in frequencies:
    total += int(frequency)
    if total in reached:
      print(total)
      duplicate_found = True
      break
    reached.add(total)
# Result Parsing