# Imports

# File IO
with open('day1.txt', 'r') as f:
  captcha = f.read()

# Actual Code
result = 0
for i in range(len(captcha) - 1,-1, -1):
  if captcha[i-1] == captcha[i]:
    result += int(captcha[i])

# Result Parsing
print result