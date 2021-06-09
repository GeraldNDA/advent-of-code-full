# Imports

# File IO
with open('day19.txt', 'r') as f:
  inpt = f.read().splitlines()

maze = [list(line) for line in inpt]
      
pos = (0, maze[0].index("|"))
dir = (1, 0) # going down
seen = ""
def mz(pos):
  if pos[0] < len(maze):
    if pos[1] < len(maze[pos[0]]):
      return maze[pos[0]][pos[1]]
step_count = 0 # get onto first one

def get_next_pos(pos, distance=1):
  return tuple(pos[i] + dir[i]*distance for i in range(len(pos)))

# Actual Code
done = False
while not done:
  next_pos = get_next_pos(pos)
  while mz(pos) != "+" and mz(next_pos) and mz(next_pos) != " ":
    if mz(pos).isalnum():
      seen += mz(pos)
    pos = next_pos
    next_pos = get_next_pos(pos)
    step_count += 1
 
  if mz(pos) == "+":
    step_count += 1
    if mz(get_next_pos(pos)) and mz(get_next_pos(pos)) != " ":
      pos = get_next_pos(pos)
    else:
      dir = (dir[1], dir[0])
      if mz(get_next_pos(pos)) and mz(get_next_pos(pos)) != " ":
       pos = get_next_pos(pos)
      else:
        dir = (-1*dir[0], -1*dir[1]) # go the opposite of new the new direction
        assert(mz(get_next_pos(pos)) and mz(get_next_pos(pos)) != " ")
        pos = get_next_pos(pos)
  elif not mz(pos) or mz(next_pos) == " ":
    if mz(pos):
      step_count += 1
      if mz(pos).isalnum():
        seen += mz(pos)
      
    done = True

# Result Parsing
print step_count