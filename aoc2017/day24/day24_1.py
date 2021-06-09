# Imports

# File IO
with open('day24.txt', 'r') as f:
  components = f.read().splitlines()
components = [tuple(map(int, component.split("/"))) for component in components]
# Actual Code
bridges = []
curr_bridges = []
# pre list components
port = 0
for component in components:
  if port in component:
    curr_bridges.append( ((component, int(not component.index(port))),) )
# connect it
done = False
while len(curr_bridges):
  for i in range(len(curr_bridges)):
    bridge = curr_bridges.pop(0)
    port = 0
    if len(bridge) == 1:
      port = max(bridge[-1][0])
    else:
      port = bridge[-1][0][bridge[-1][1]]
    simple_bridge = map(lambda x: x[0], bridge)
    for component in components:
      if component not in simple_bridge:
        if port in component:
          curr_bridges.append(bridge + ((component, int(not component.index(port))),) )
    else:
      bridges.append(bridge)

# for bridge in bridges:
  # print map(lambda x: x[0], bridge)
# print len(bridges), components
# Result Parsing
def sum_up(bridge):
  simple_bridge = map(lambda x: x[0], bridge)
  return sum(sum(component) for component in simple_bridge)

max_bridges = [max(bridges, key=len)]
max_bridge_len = len(max_bridges[0])
for bridge in bridges:
  if len(bridge) == max_bridge_len:
    max_bridges.append(bridge)

print sum_up(max(max_bridges, key=sum_up))