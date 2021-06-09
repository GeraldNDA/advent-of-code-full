# Imports
from collections import defaultdict

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
done = False
weight_tree = {}
while not done:
  children = tree[base_node]
  subtree_weights = {}
  for child in children:
    subtree_weights[child] = calc_tree_weight(child, tree, weights)
  weight_tree[base_node] = dict(subtree_weights)
  
  unique_weight = [program for program in subtree_weights.keys() if subtree_weights.values().count(subtree_weights[program]) == 1]
  if len(unique_weight) != 1:
    print unique_weight, subtree_weights
    break
  else:
    base_node = unique_weight.pop()
          
# Result Parsing
print  base_node, weights[base_node]
parent = reverse_tree[base_node][0]
goal_weight = [weight for weight in set(weight_tree[parent].values()) if weight != weight_tree[parent][base_node]].pop()
result = weights[base_node] + (goal_weight - weight_tree[parent][base_node])
print result