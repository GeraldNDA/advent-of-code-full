# Imports
from itertools import combinations

# File IO
with open('day2.txt', 'r') as f:
  spreadsheet = f.read().splitlines()

# Actual Code
result = 0
for line in spreadsheet:
  row = [int(cell) for cell in line.split("\t")]
  for combo in combinations(row, 2):
    if max(combo) % min(combo) == 0:
      result += max(combo) / min(combo)
      break

# Result Parsing
print result