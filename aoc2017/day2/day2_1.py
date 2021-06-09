# Imports

# File IO
with open('day2.txt', 'r') as f:
  spreadsheet = f.read().splitlines()

# Actual Code
result = 0
for line in spreadsheet:
  row = [int(cell) for cell in line.split("\t")]
  result += max(row) - min(row)

# Result Parsing
print result