# Imports
from collections import defaultdict

# File IO
with open('day18.txt', 'r') as f:
  instructions = f.read().splitlines()

# Actual Code
send_counts = defaultdict(lambda: 0)

class Program:
  def __init__(self, id):
    self.id = id
    
    self.registers = defaultdict(lambda: 0)
    self.registers['p'] = id
    
    self.ip = 0
    self.max_ip = 0
    
    self.waiting = False
    self.dead = False
    self.queue = []

    
  def run(self, other):
    if self.waiting or self.ip >= len(instructions):
      if self.ip >= len(instructions):
        self.dead = True
      return
    instruction = instructions[self.ip].split(" ")
    def get_value(i):
      val = 0
      if instruction[i].lstrip("+-").isdigit():
        val = int(instruction[i])
      else:
        val = self.registers[instruction[i]]
      return val
      
    if instruction[0] == "set":
      val = get_value(2)
      self.registers[instruction[1]] = val
    elif instruction[0] == "add":
      val = get_value(2)
      self.registers[instruction[1]] +=  val
    elif instruction[0] == "mul":
      val = get_value(2)
      self.registers[instruction[1]] *= val
    elif instruction[0] == "mod":
      val = get_value(2)
      self.registers[instruction[1]] = self.registers[instruction[1]] % val
    
    elif instruction[0] == "rcv":
      if self.queue:
        self.registers[instruction[1]] = self.queue.pop(0)
      else:
        self.waiting = True
        self.ip -= 1
        
    elif instruction[0] == "snd":
      val = get_value(1)
      other.waiting = False
      other.queue.append(val)
      send_counts[self.id] += 1
      
    elif instruction[0] == "jgz":
      if self.registers[instruction[1]] > 0:
        val = get_value(2)
        self.ip += val - 1
    else:
      print "Something went wrong!!!"
      print instruction[0]
    self.ip += 1
    self.max_ip = max(self.ip, self.max_ip)
    print self.id,self.max_ip, "\r",
      
prog0 = Program(0)
prog1 = Program(1)

done = False
def run_program(program, other):
  program.run(other)
  if (program.waiting or program.dead) and (other.waiting or other.dead):
    # end thread
  
while not done:
  prog0.run(prog1)
  prog1.run(prog0)
  
  if (prog0.waiting or prog0.dead) and (prog1.waiting or prog1.dead):
    done = True
  # print send_counts, "\r",
  # print len(prog0.queue), len(set(prog0.queue)), len(prog1.queue), len(set(prog1.queue)), "\r",
    
  



# Result Parsing
print send_counts