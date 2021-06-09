# Imports
import sys
from itertools import combinations
from copy import deepcopy
from collections import defaultdict

# File IO
with open('day20.txt', 'r') as f:
  particles = f.read().splitlines()

parts = []
for particle in particles:
  particle.strip(" ")
  particle = map(lambda x: x.strip(",").split("="), particle.split(" "))
  motions = map(lambda x: x[0], particle)
  values = map(lambda x: x[1].strip("<>").split(","), particle)
  values = map(lambda x: tuple(map(lambda y: int(y.strip()), x)),values)
  particle = dict(zip(motions, values))
  parts.append(particle.copy())
def passes_origin(prev, curr):
  # if either prev or curr is 0, then true
  # if opposite sign (product is negative) then true
  # if same sign (product is positive) then false
  return prev * curr <= 0

def collide(partA, partB):
  partA = partA.copy()
  partB = partB.copy()
  # convert to  B in reference to abs
  partB = {k: tuple(partB[k][i] - partA[k][i] for i in range(3)) for k in partB}
  return is_collide(partB)
  
def tick(part):
  part = part.copy()
  part["v"] = tuple(part["v"][dim] + part["a"][dim] for dim in range(3))
  part["p"] = tuple(part["p"][dim] + part["v"][dim] for dim in range(3))
  return part
def collision_time(prev_pos, part):
  # what percentage of velocity will give 0,0,0 if any?
  time = None
  tolerance = 0
  for dim in range(3):
    displacement = part['p'][dim]
    # previously applied velocity
    velocity = part['v'][dim] - part['a'][dim]
    if not time:
      collision_time = float(displacement)/float(velocity) if velocity != 0 else 0
      assert 0 <= collision_time <= 1, (
        "\nCollision Time: " + str(collision_time) +
        "\nCollision Displacement: " + str(displacement) +
        "\nCollision Velocity: " + str(velocity) +
        "\nDimension: " + str(dim) +
        "\nPrev Position: " + str(prev_pos) +
        "\nParticle: " + str(part))
      time = collision_time
    elif not abs(displacement - velocity * time) <= tolerance:
      return False
  return time

def is_collide(part):
  prev_pos = part['p']
  part = part.copy()
  ticks = 0
  while True:
    if all(not part['p'][dim] for dim in range(3)):
      print part['p'],
      return ticks
    # passes through each other
    # if all(passes_origin( prev_pos[dim], part['p'][dim] ) for dim in range(3)):
      # return ticks
      # time = collision_time(prev_pos, part)
      # if time != False or time is 0:
        # return ticks + time
    for dim in range(3):
      if all(not part[k][dim] for k in part):
        continue
      elif all(part[k][dim] >= 0 for k in part):
        return False
      elif all(part[k][dim] <= 0 for k in part):
        return False
    prev_pos = part['p']
    part = tick(part)
    ticks += 1

deleted = []
deletions = defaultdict(list)
for (i, j) in combinations(range(len(parts)), 2):
  print i, j, "\r",
  sys.stdout.flush()
  ticks = collide(parts[i], parts[j])
  if ticks != False:
    # print i, j, ticks
    deletions[ticks].append((i,j))
for time in sorted(deletions.keys()):
  to_delete = set()
  for (i, j) in deletions[time]:
    if i not in deleted and j not in deleted:
      to_delete.add(i)
      to_delete.add(j)
  deleted.extend(to_delete)

print "=== NEVER COLLIDE ==="
print len(parts) - len(deleted)
