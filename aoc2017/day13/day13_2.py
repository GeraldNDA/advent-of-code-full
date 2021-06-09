# Imports
from collections import defaultdict

# File IO
with open('day13.txt', 'r') as f:
  inpt = f.read().splitlines()

#depth => range
firewall = defaultdict(lambda: 0)
for line in inpt:
  line = [word.strip() for word in line.split(":")]
  firewall[int(line[0])] = int(line[1])

# Actual Code
def is_caught(start):
  max_depth = max(firewall.keys()) 
  for depth in range(max_depth + 1):
    rnge = firewall[depth]
    if rnge > 0:
      scanner_pos = (depth + start) % (2* (rnge - 1))
      
      if scanner_pos >= range:
        scanner_pos = (2*(rnge - 1)) - scanner_pos
      if not scanner_pos:
        return True
    else:
      continue
  return False

delay = 0
while is_caught(delay):
  delay += 1
    
  

# Result Parsing
print delay