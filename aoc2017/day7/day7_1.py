# Imports
from copy import deepcopy
from collections import defaultdict

def recursive_defaultdict():
  return defaultdict(recursive_defaultdict)

# File IO
with open('day7.txt', 'r') as f:
  program_map = f.read().splitlines()

# Actual Code
tree = defaultdict(list)
reverse_tree = defaultdict(list)
weights = {}

for line in program_map:
  line = line.split(" ")
  program_name = line[0]
  sub_programs = []
  weights[program_name] = int(line[1].strip("(").strip(")"))
  if len(line) > 3:
    sub_programs = [sub_program.strip(",") for sub_program in line[3:]]
  
  tree[program_name] = list(sub_programs)
  for sub_program in sub_programs:
    reverse_tree[sub_program].append(program_name)

def calc_tree_weight(child, tree, weights):
  if len(tree[child]) == 0:
    return weights[child]
  sum = weights[child]
  for sub_child in tree[child]:
    sum += calc_tree_weight(sub_child, tree, weights)
  return sum

base_node = (set(tree.keys()) - set(reverse_tree.keys())).pop()

# Result Parsing
print  base_node