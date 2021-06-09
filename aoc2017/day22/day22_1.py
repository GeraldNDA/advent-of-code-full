# Imports

# File IO
with open('day22.txt', 'r') as f:
  inpt = f.read().splitlines()
cluster = [list(line) for line in inpt]

# Actual Code

#          up  | right| down | left
dirs = ((-1, 0), (0,1), (1,0),(0,-1))
direction = 0

infected = set()

for r in range(len(cluster)):
  for c in range(len(cluster)):
    if cluster[r][c] == "#":
      infected.add((r,c))

curr_pos = (len(cluster)/2, len(cluster)/2)

become_infected = 0
for i in range(10000):
  if curr_pos in infected:
    direction = (direction + 1) % 4
    infected.remove(curr_pos)

  else:
    direction = (direction - 1) % 4
    infected.add(curr_pos)
    become_infected += 1
  
  curr_pos = (curr_pos[0] + dirs[direction][0], curr_pos[1] + dirs[direction][1])

# Result Parsing
print become_infected
