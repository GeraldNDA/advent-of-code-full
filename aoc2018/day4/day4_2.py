#!/usr/bin/env python3
# Imports
from datetime import datetime, timedelta
import re
from collections import defaultdict

START_SHIFT_PATTERN = r"^Guard #(\d+) begins shift$"
FALLS_ASLEEP_PATTERN = r"^falls asleep$"
WAKE_UP_PATTERN = r"^wakes up$"
# File IO
def parse_record_line(line):
  record_info = line.split(" ", 2)
  record_info[0] = " ".join(record_info[:2])
  record_info.pop(1)
  record_info[0] = datetime.strptime(record_info[0], "[%Y-%m-%d %H:%M]")
  return tuple(record_info)

with open('day4.txt', 'r') as f:
  guard_record = list(map(parse_record_line, f.read().splitlines()))
guard_record = dict(guard_record)

# Actual Code
guard_stats = defaultdict(list)
last_guard = None
first_time = None
for time in sorted(guard_record.keys()):
  first_time = time
  break

for time in sorted(guard_record.keys()):
  guard_info = guard_record[time]
  if re.search(START_SHIFT_PATTERN, guard_info):
    info = re.match(START_SHIFT_PATTERN, guard_info)
    last_guard = info.group(1)
  elif re.search(FALLS_ASLEEP_PATTERN, guard_info):
    guard_stats[last_guard].append(dict(sleep_start=time, sleep_time=timedelta(0)))
  elif re.search(WAKE_UP_PATTERN, guard_info):
    guard_stats[last_guard][-1]["sleep_end"] = time
    guard_stats[last_guard][-1]["sleep_time"] = guard_stats[last_guard][-1]["sleep_end"] - guard_stats[last_guard][-1]["sleep_start"]

guards = list(guard_stats.keys())
def best_min(guard):
  minutes_asleep = [0]*60
  for info in guard_stats[guard]:
    if info["sleep_time"]:
      time = info["sleep_start"]
      while time != info["sleep_end"]:
        minutes_asleep[time.minute] += 1
        time += timedelta(seconds=60)
  most_sleep_min = max(range(60), key=lambda t: minutes_asleep[t])
  return (most_sleep_min, minutes_asleep[most_sleep_min])

def most_sleep_same_min(guard):
  return best_min(guard)[1]

guards.sort(key=most_sleep_same_min)
# Result Parsing
guard = guards[-1]
most_sleep_min = best_min(guards[-1])[0]
print(guard, most_sleep_min, int(guard)*int(most_sleep_min))