# Imports

# File IO
with open('day6.txt', 'r') as f:
  banks = f.read().strip()

# Actual Code
configs = []
banks = map(int, banks.split("\t"))
bankCount = len(banks)
i = 0
done = False
while not done:
  configs.append(tuple(banks))
  bankToAlter = banks.index(max(banks))
  j = bankToAlter + 1
  blocks = banks[bankToAlter]
  banks[bankToAlter] = 0
  while blocks > 0:
    j = j % bankCount
    banks[j] += 1
    blocks -= 1
    j+=1
  if tuple(banks) in configs:
    done = True
  i += 1
  

# Result Parsing
print i