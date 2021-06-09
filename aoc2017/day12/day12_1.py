# Imports
from collections import defaultdict
# File IO
with open('day12.txt', 'r') as f:
  pipes = f.read().splitlines()

# Actual Code
tree = defaultdict(set)
connections = defaultdict(set)

for line in pipes:
  pipe = line.split(" ")
  frm = pipe[0]
  to = set(info.strip(",") for info in pipe[2:])
  tree[frm] = to
  for program in to:
    tree[program].add(frm)

for program in tree:
  connections[program].add(program)
  friends = list(tree[program])
  
  while len(friends):
      friend = friends.pop(0)        
      if friend not in connections[program]:
        # don't loop infitely
        connections[program].add(friend)
        for far_friend in tree[friend]:
          if far_friend not in connections[program]:
            friends.append(far_friend)
            


# Result Parsing
print len(connections["0"])