#!/usr/bin/env python3
# Imports

# File IO
  
with open('day5.txt', 'r') as f:
  polymer = f.read()
polymer = list(polymer)
# Actual Code
idx = 0
original_len = len(polymer)
while idx < len(polymer) - 1:
  if polymer[idx] != polymer[idx + 1]:
    if polymer[idx].upper() ==  polymer[idx + 1].upper():
      del polymer[idx:idx+2]
      if idx > 0:
        idx -= 1
      idx -= 1
  idx += 1
  print("PROGRESS, current:", idx, "original_len:", original_len, end="\r")

# Result Parsing
print()
print(len(polymer))