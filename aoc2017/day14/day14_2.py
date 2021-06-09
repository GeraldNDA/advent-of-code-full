# Imports

# File IO
# with open('day14.txt', 'r') as f:
#key_str = "flqrgnkx"
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

def is_valid(grid_pos):
  if 0 <= grid_pos[0] < 128:
    if 0 <= grid_pos[1] < 128:
      return True
  return False
# Actual Code
grid = []
for j in range(128):
  row_key = "{}-{}".format(key_str, j)
  row_hash = knot_hash(row_key)
  grid_row = list()
  for chr in row_hash:
    grid_row.extend( map(int, list("{0:b}".format(int(chr, 16)).zfill(4)) ))
  grid.append(grid_row)

dirs = [
  (0, -1),
  (0, 1),
  (1, 0),
  (-1, 0)
]
# simplified afterwards to remove unneccessary variables etc.
regions = 0
touched = set()
for i in range(128):
  for j in range(128):
    cell = (i, j)
    if cell in touched:
      continue
    if not grid[cell[0]][cell[1]]:
      continue
    touched.add(cell)
    search = [cell]
    while len(search):
      for item in range(len(search)):
        sqr = search.pop(0)
        for dir in dirs:
          neighbour = (sqr[0] + dir[0], sqr[1] + dir[1])
          if is_valid(neighbour) and neighbour not in touched:
            if grid[neighbour[0]][neighbour[1]]:
              touched.add(neighbour)
              search.append(neighbour)
    regions += 1
    print i, "\r",
              
        
# Result Parsing
print regions