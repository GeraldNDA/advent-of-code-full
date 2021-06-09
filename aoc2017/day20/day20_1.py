# Imports

# File IO
with open('day20.txt', 'r') as f:
  particles = f.read().splitlines()


# Actual Code
particle_info = []
current_min = 0
for info in particles:
  info = [stat.strip(",").split("=") for stat in info.split(" ")]
  info = dict(map(lambda x: (x[0],map(int, x[1].strip("<>").split(","))) , info))
  particle_info.append(info)
  # create a score out of this number
  idx = len(particle_info) - 1
  min_particle = particle_info[current_min]
  min_score = {
    'a': sum(map(abs, min_particle['a'])),
    'v': sum(map(abs, min_particle['v'])),
    'p': sum(map(abs, min_particle['p']))
  }
  curr_score = {
    'a': sum(map(abs, info['a'])),
    'v': sum(map(abs, info['v'])),
    'p': sum(map(abs, info['p']))
  }
  if curr_score['a'] < min_score['a']:
    current_min = idx
  elif curr_score['a'] == min_score['a']:
    if curr_score['v'] < min_score['v']:
      current_min = idx
    elif curr_score['v'] == min_score['v']:
      if curr_score['p'] < min_score['p']:
        current_min = idx
# Result Parsing
print current_min