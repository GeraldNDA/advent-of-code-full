#!/usr/bin/env python3
# Imports

# File IO
  
with open('day5.txt', 'r') as f:
  polymer = f.read()
polymer = list(polymer)
# Actual Code
def reacted_length(reacting_polymer):
  idx = 0
  while idx < len(reacting_polymer) - 1:
    if reacting_polymer[idx] != reacting_polymer[idx + 1]:
      if reacting_polymer[idx].upper() ==  reacting_polymer[idx + 1].upper():
        del reacting_polymer[idx:idx+2]
        if idx > 0:
          idx -= 1
        idx -= 1
    idx += 1
  return len(reacting_polymer)

units = set("".join(polymer).upper())
unit_count = len(units)
min_length = len(polymer)
amount = 0
for unit in units:
  amount += 1
  curr_polymer = list(filter(lambda u: u.upper() != unit, polymer))
  min_length = min(reacted_length(curr_polymer), min_length)
  print("DONE: {}/{}".format(amount, unit_count), end="\r")
print()
print(min_length)
