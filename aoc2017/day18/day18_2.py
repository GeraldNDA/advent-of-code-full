# Imports
from collections import defaultdict

# File IO
with open('day18.txt', 'r') as f:
  instructions = f.read().splitlines()

# Actual Code
send_counts = {0:0, 1:0}

class Program:
  def __init__(self, id):
    self.id = id
    
    self.registers = defaultdict(lambda: 0)
    self.registers['p'] = id
    
    self.ip = 0
    self.waiting = False
    self.dead = False
    self.queue = []
    
  def run(self, other):
      if self.waiting or self.ip >= len(instructions):
        return
      if self.ip >= len(instructions):
        self.dead = True
        return
      
      instruction = instructions[self.ip].split(" ")
      def get_value(i):
        v = 0
        if instruction[i].lstrip("+-").isdigit():
          v = int(instruction[i])
        else:
          v = self.registers[instruction[i]]
        return v
      
      if len(instruction) > 2:
        val = get_value(2)
        
      if instruction[0] == "set":
        self.registers[instruction[1]] = val
      elif instruction[0] == "add":
        self.registers[instruction[1]] +=  val
      elif instruction[0] == "mul":
        self.registers[instruction[1]] *= val
      elif instruction[0] == "mod":
        self.registers[instruction[1]] = get_value(1) % val
      
      elif instruction[0] == "rcv":
        
        if self.queue:
          self.waiting = False
          self.registers[instruction[1]] = self.queue.pop(0)
        else:
          self.waiting = True
          self.ip -= 1
          
      elif instruction[0] == "snd":
        val = get_value(1)
        other.queue.append(val)
        other.waiting = False
        send_counts[self.id] += 1
        
      elif instruction[0] == "jgz":
        
        if get_value(1) > 0:
          self.ip += val - 1
      else:
        print "Something went wrong!!!"
        print instruction[0]
      self.ip += 1
      if not all(key.isalpha() for key in self.registers.keys()):
        self.dead = True
        print instruction, dict(self.registers)
prog0 = Program(0)
prog1 = Program(1)

done = False
while not done:
  prog0.run(prog1)
  prog1.run(prog0)
  
  if (prog0.waiting or prog0.dead) and (prog1.waiting or prog1.dead):
    done = True
  

# Result Parsing
print dict(send_counts)