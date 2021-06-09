# Imports

# File IO
with open('day9.txt', 'r') as f:
  inpt = f.read()

# Actual Code
score = 0
group_depth = 0
garbage = False
skip = False
for chr in inpt:
  if skip:
    skip = False
    continue
  
  if chr == "<" and not garbage:
    garbage = True
    continue
  elif chr == ">":
    garbage = False
    continue

  if garbage:
    if chr == "!":
      skip = True
    else:  
      # print chr
      score += 1
  else:
    if chr == "{":
      group_depth += 1
    elif chr == "}":
      group_depth -= 1

# Result Parsing
print score