# Imports

# File IO
# key_str = "flqrgnkx"
key_str = "ugkiagan"

# calc knot hash
def reverse_range(lst, start, length):
  #pre turn
  rnge = lst[start:start+length]
  extra_distance = length - (len(lst) - start)
  if extra_distance > 0:
    rnge.extend(lst[0:extra_distance])
  for i in range(length):
    reverse_idx = length - i - 1
    i = i + start
    i = i % len(lst)
    lst[i] = rnge[reverse_idx]
    
def xor_accumulate(lst):
  total = 0
  for i in lst:
    total = i ^ total
  return total

def knot_hash(key):
  lst = range(256)
  lengths = map(ord, key) + [17, 31, 73, 47, 23]
  curr_pos = 0
  skip = 0
  for i in range(64):
    for length in lengths:
      reverse_range(lst, curr_pos, length)
      curr_pos += length + skip
      curr_pos = curr_pos % len(lst)
      skip += 1

  dense_hash = ""
  for i in range(16):
    dense_hash += "{:02x}".format(xor_accumulate(lst[i*16:i*16+16]))
  return dense_hash

# Actual Code
result = 0
grid = []
accumulate = 0
for j in range(128):
  row_key = "{}-{}".format(key_str, j)
  row_hash = knot_hash(row_key)
  grid_row = list()
  for chr in row_hash:
    grid_row.extend( map(int, list("{0:b}".format(int(chr, 16)).zfill(4)) ))
  accumulate += sum(grid_row)
  grid.append(grid_row)

# Result Parsing
print accumulate