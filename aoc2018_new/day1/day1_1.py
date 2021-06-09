#!/usr/bin/env python3
# Imports

# File IO
with open('day1.txt', 'r') as f:
  frequencies = f.readlines()


# Actual Code
frequencies = map(int, frequencies)
# Result Parsing
print(sum(frequencies))