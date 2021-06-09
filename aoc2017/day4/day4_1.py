# Imports

# File IO
with open('day4.txt', 'r') as f:
  passphrases = f.read().splitlines()

# Actual Code
valid_count = 0
for phrase in passphrases:
  phrase = phrase.split(" ")
  valid = True
  for word in phrase:
    if phrase.count(word) != 1:
      valid = False
  if valid:
    valid_count += 1

# Result Parsing
print valid_count