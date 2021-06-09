# Imports

# File IO
with open('day4.txt', 'r') as f:
  passphrases = f.read().splitlines()

  
def is_anagram(word1, word2):
  anagram = True
  for letter in set(word1).union(set(word2)):
    if word1.count(letter) != word2.count(letter):
        anagram = False
        break
  return anagram
        
# Actual Code
valid_count = 0
for phrase in passphrases:
  phrase = phrase.split(" ")
  valid = True
  for i in range(len(phrase)):
    for j in range(len(phrase)):
      # skip same word
      if i == j:
        continue
      else:
        word = phrase[i]
        test = phrase[j]
     
      if is_anagram(test, word):
        valid = False
        break
    if not valid:
      break
      
  if valid:
    valid_count += 1

# Result Parsing
print valid_count