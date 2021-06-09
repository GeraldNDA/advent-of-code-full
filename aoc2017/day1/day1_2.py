# Imports

# File IO
with open('day1.txt', 'r') as f:
  captcha = f.read().splitlines()
captcha = captcha[0]

# Actual Code
result = 0
halfway = len(captcha)/2
for i in range(len(captcha) - 1,-1, -1):
  if captcha[i-halfway] == captcha[i]:
    result += int(captcha[i])

# Result Parsing
print result