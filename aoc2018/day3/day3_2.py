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

def is_unique(x_start, y_start, width, height):
  for x in range(x_start, x_start + width):
    for y in range(y_start, y_start + height):
      if fabric[y][x] != 1:
        return False
  return True

for claim in elf_claims:
  claim = claim.split(" ")
  claim_id = claim[0].strip("#")
  x_start, y_start = claim[2].split(",")
  width, height = claim[3].split("x")
  y_start = y_start.strip(":")
  x_start, y_start, width, height = map(int, [x_start, y_start, width, height])
  if is_unique(x_start, y_start, width, height):
    print(claim_id)
    break
# print(done)