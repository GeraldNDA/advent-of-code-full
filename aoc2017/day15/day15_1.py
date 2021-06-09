# Imports

# File IO
a_start = 679
b_start = 771
# Test
# a_start = 65
# b_start = 8921

# Actual Code
def gen_a(start):
  current = start
  while True:
    current = ( current * 16807 ) % 2147483647
    yield current

def gen_b(start):
  current = start
  while True:
    current = ( current * 48271 ) % 2147483647
    yield current

a = gen_a(a_start)
b = gen_b(b_start)

score = 0
sixteen_zeros = "0"*16
for i in range(40000000):
  a_dec = a.next()
  b_dec = b.next()
  
  bin_result = '{0:16b}'.format(a_dec ^ b_dec)
  if bin_result.endswith(sixteen_zeros):
    score = score + 1
  
  # print i, "\r",
    
# Result Parsing
print score