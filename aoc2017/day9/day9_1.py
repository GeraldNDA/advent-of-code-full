# Imports

# File IO
with open('day9.txt', 'r') as f:
  inpt = f.read()

# Actual Code
score = 0
group_count = 0
group_depth = 0
garbage = False
skip = False
for chr in inpt:
  if skip:
    skip = False
    continue
  
  if chr == "<":
    garbage = True
  elif chr == ">":
    garbage = False
  elif chr == "!" and garbage:
    skip = True
  if not garbage:
    if chr == "{":
      group_depth += 1
    elif chr == "}":
      score += group_depth
      group_depth -= 1
  

# Result Parsing
print score