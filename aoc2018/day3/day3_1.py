#!/usr/bin/env python3
# Imports

# File IO
with open('day3.txt', 'r') as f:
  elf_claims = f.read().splitlines()

# Actual Code
fabric = [[0]*1000 for i in range(1000)]

for claim in elf_claims:
  claim = claim.split(" ")
  x_start, y_start = claim[2].split(",")
  width, height = claim[3].split("x")
  y_start = y_start.strip(":")
  x_start, y_start, width, height = map(int, [x_start, y_start, width, height])
  for x in range(x_start, x_start + width):
    for y in range(y_start, y_start + height):
      fabric[y][x] += 1

inches_used = sum(len(list(filter(lambda v: v >= 2, row))) for row in fabric)
print(inches_used)