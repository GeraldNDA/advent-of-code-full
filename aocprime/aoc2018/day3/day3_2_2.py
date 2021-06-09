#!/usr/bin/env python3
## IMPROVEMENTS
# Imports

# File IO
def elf_claim_parser(line):
  claim = line.split(" ")
  claim_info = {}
  claim_id = claim[0].strip("#")
  x_start, y_start = claim[2].split(",")
  width, height = claim[3].split("x")
  y_start = y_start.strip(":")
  x_start, y_start, width, height = map(int, [x_start, y_start, width, height])
  return dict(
    id=claim_id,
    x_start=x_start,
    y_start=y_start,
    width=width,
    height=height
  )

with open('day3.txt', 'r') as f:
  elf_claims = list(map(elf_claim_parser, f.read().splitlines()))
# Actual Code
fabric = [[0]*1000 for i in range(1000)]

for claim in elf_claims:
  for x in range(claim["x_start"], claim["x_start"] + claim["width"]):
    for y in range(claim["y_start"], claim["y_start"] + claim["height"]):
      fabric[y][x] += 1

def is_unique(claim):
  for x in range(claim["x_start"], claim["x_start"] + claim["width"]):
    for y in range(claim["y_start"], claim["y_start"] + claim["height"]):
      if fabric[y][x] != 1:
        return False
  return True

for claim in elf_claims:
  if is_unique(claim):
    print(claim["id"])
    break