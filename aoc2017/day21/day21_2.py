# Imports
def expand_rule(x):
  return map(list, x.split("/"))

# File IO
with open('day21.txt', 'r') as f:
  rules = f.read().splitlines()

rules = map(lambda rule: rule.split(" ")[::2] , rules)
rules = map(lambda rule: map(expand_rule, rule), rules)
print rules[0]


# Actual Code
# Start
# .#.
# ..# 
# ###
def orientations(pattern):
  #regular
  yield pattern
  # flip horizontal
  yield map(lambda x: x[::-1], pattern)
  # flip vertical
  yield pattern[::-1]
  size = len(pattern)
  
  for i in range(3):
    rotated_pattern = [list() for i in range(size)]
    for row in pattern:
      for val in range(size):
        rotated_pattern[val].insert(0, row[val])
    yield rotated_pattern
    # flip horizontal
    yield map(lambda x: x[::-1], rotated_pattern)
    # flip vertical
    yield rotated_pattern[::-1]
    pattern = rotated_pattern
    
  
def search_rules(search):
  search = map(list, search) # duplicate
  for orientation in orientations(search):
    for rule in rules:
      # print orientation, rule[0]
      if len(rule[0]) == len(search):
        if rule[0] == orientation:
          return rule[1]
  return False
    
      
    

image = [list(".#."), list("..#"), list("###")]
for line in image:
  print "".join(line)
for x in range(18):
  size = len(image)
  new_image = []
  if not size % 2:
    for i in range(size/2):
      for j in range(size/2):
        r = (i*2, (i+1)*2)
        c = (j*2, (j+1)*2)
        # get range
        rnge = map(lambda y: y[c[0]:c[1]], image[r[0]:r[1]])
        mapping = search_rules(rnge)
        
        # add map result to line
        idx = 0
        for line in mapping:
          if not c[0]:
            new_image.append(list(line))
          else:
            new_image[i*len(mapping) + idx].extend(line)
          idx += 1
  elif not size % 3:
    for i in range(size/3):
      for j in range(size/3):
        r = (i*3, (i+1)*3)
        c = (j*3, (j+1)*3)
        # get range
        rnge = map(lambda y: y[c[0]:c[1]], image[r[0]:r[1]])
        mapping = search_rules(rnge)
        
        # add map result to line
        idx = 0
        for line in mapping:
          if not c[0]:
            new_image.append(list(line))
          else:
            new_image[i*len(mapping) + idx].extend(line)
          idx += 1
  image = map(list, new_image)
  print x
# Result Parsing

print sum([x.count("#") for x in image])
  
