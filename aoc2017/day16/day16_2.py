# Imports

# File IO
with open('day16.txt', 'r') as f:
  dance = f.read()
# dance = "s1,x3/4,pe/b"

# Actual Code
def spin(x):
  x[0],x[1:] =  x[-1], x[:-1]

def exchange(lst, x, y):
  lst[x], lst[y] = lst[y], lst[x]

def partner(lst, x, y):
  exchange(lst, lst.index(x), lst.index(y))

def apply_step(dncers, step):
  if step[0] == "s":
      for move in range(int(step[1:])):
        spin(dncers)
  if step[0] == "x":
    programs = map(int, step[1:].split("/"))
    exchange(dncers, *programs)
  if step[0] == "p":
    programs = step[1:].split("/")
    partner(dncers, *programs)

dance_steps = dance.split(",")
dancers = list("abcdefghijklmnop")
# dancers = list("abcde")

done = False
final_pos = ["".join(dancers)]
while not done:
  for step in dance_steps:
    apply_step(dancers, step)
  signature = "".join(dancers)
  if signature in final_pos:
    break
  final_pos.append("".join(dancers))
# Result Parsing
print final_pos[1000000000 % len(final_pos)]