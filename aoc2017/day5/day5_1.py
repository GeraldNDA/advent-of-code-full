# Imports

# File IO
with open('day5.txt', 'r') as f:
  input = list(map(int, f.read().splitlines()))

# Actual Code
result = 0
i = 0

while(i < len(input)):
  t = input[i]
  input[i] += 1
  i += t
  result += 1
# Result Parsing
print result