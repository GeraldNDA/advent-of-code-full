# Imports
from collections import defaultdict

# File IO
with open('day23.txt', 'r') as f:
  instructions = f.read().splitlines()

# Actual Code
class Program:
  def __init__(self):
    self.registers = defaultdict(lambda: 0)
    # self.registers["a"] = 0
    
    self.ip = 0
    self.dead = False
    self.mul_count = 0
    
  def get_val(self, instruction, i):
    if len(instruction) >= i + 1:
      if instruction[i].lstrip("+-").isdigit():
        return int(instruction[i])
      else:
        return self.registers[instruction[i]]
    return 0
    
  def run(self):
    print self.ip, 
    prev_val = self.registers.copy()
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
      self.mul_count += 1
    elif instruction[0] == "jnz":
      if self.get_val(instruction, 1) != 0:
        self.ip += val - 1
        self.last_line = self.ip + 1
        self.last_jump = instruction
    else:
      print "Something went wrong!!!"
      print instruction[0]
      self.dead = True
    if self.ip < len(instructions) and prev_val["f"] != self.registers['f']:
      print dict(co_processor.registers), dict(prev_val), self.ip, instructions[self.ip]
    self.ip += 1
     
    print dict(co_processor.registers), "\r",

co_processor = Program()
while not co_processor.dead:
  co_processor.run()
  

# Result Parsing
print co_processor.mul_count, 