# Imports
import sys
from collections import defaultdict

# File IO
with open('day23.txt', 'r') as f:
  instructions = f.read().splitlines()
  
# Actual Code
class Program:
  def __init__(self):
    self.registers = defaultdict(lambda: 0)
    self.registers["a"] = 1
    self.ip = 0
    self.dead = False
    
  def get_val(self, instruction, i):
    if len(instruction) >= i + 1:
      if instruction[i].lstrip("+-").isdigit():
        return int(instruction[i])
      else:
        return self.registers[instruction[i]]
    return 0
    
  def run(self):
    if self.ip >= len(instructions):
      self.dead = True
      return
    
    # get value 
    instruction = instructions[self.ip].split(" ")
    val = self.get_val(instruction, 2)
    if instruction[0] == "set":
      self.registers[instruction[1]] = val
    elif instruction[0] == "sub":
      self.registers[instruction[1]] -=  val
    elif instruction[0] == "mul":
      self.registers[instruction[1]] *= val
    elif instruction[0] == "mod":
      self.registers[instruction[1]] = self.get_val(instruction, 1) % val
    elif instruction[0] == "sqrt":
      self.registers[instruction[1]] = int(val ** 0.5) + 1

    elif instruction[0] == "jnz":
      if self.get_val(instruction, 1) != 0:
        self.ip += val - 1
    else:
      print "Something went wrong!!!"
      print instruction[0]
      self.dead = True
    self.ip += 1
      
co_processor = Program()
while not co_processor.dead:
  co_processor.run()
  if co_processor.ip >= 9:
      co_processor.dead = True

# register a is whether start = end or not ("DEBUG MODE")
# register b is where the loop starts
# register c is where it ends
# register d and e are the numbers to multiply to check if b is composite
# register f stores if b is composite
# register g is for random calculations
# register h is a count of how many composite numbers there are4

# optimized version
start = co_processor.registers['b']
end = co_processor.registers['c']
print start
print end
composite_count = 0
while start != end:
  for i in xrange(2,start):
    if start % i == 0:
      composite_count += 1
      break
  start += 17

for i in xrange(2,start):
  if start % i == 0:
    composite_count += 1
    break
print composite_count

# Other ideas for optimization
# This code runs the assembly version of above
# add new command mod where mod X Y means x = x % y (reflected in Program already)


with open('day23_2.txt', 'r') as f:
  instructions = f.read().splitlines()
  
co_processor = Program()
while not co_processor.dead:
  co_processor.run()
  print co_processor.ip,co_processor.registers['h'], dict(co_processor.registers), "\r",
print co_processor.registers['h']