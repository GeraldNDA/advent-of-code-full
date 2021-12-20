#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from operator import methodcaller
from typing import List

# Input Parse
puzzle = AdventOfCode(year=2021, day=8)
puzzle_input = puzzle.get_input()

example = [
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
]
# puzzle_input = example

# Actual Code
class Signal:
    def __init__(self, signal_patterns: List[str], output_value: List[str]) -> None:
        self.signal_patterns = signal_patterns
        self.output_value = output_value

    def num_easy_outputs(self):
        num_easy = 0
        for n in self.output_value:
            if len(n) in (2, 4, 3, 7):
                num_easy += 1
        return num_easy

    def decode(self):
        patterns = set()
        value_map = {}
        for n in self.signal_patterns:
            n = "".join(sorted(n))
            if len(n) == 2:
                value_map[n] = 1
            elif len(n) == 4:
                value_map[n] = 4
            elif len(n) == 3:
                value_map[n] = 7
            elif len(n) == 7:
                value_map[n] = 8
            else:
                patterns.add(n)
                continue
        reverse_value_map = {v: k for k,v in value_map.items()}

        for n in patterns:
            n = "".join(sorted(n))
            if n in value_map:
                continue
            if len(n) == 6:
                missing_letter = set(reverse_value_map[8]) - set(n)
                missing_letter = missing_letter.pop()
                if not any((missing_letter in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                    value_map[n] = 9
                elif all((missing_letter in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                    value_map[n] = 6
                elif missing_letter in reverse_value_map[4] and not any((missing_letter in disp) for disp in  map(reverse_value_map.get, (1,7))):
                    value_map[n] = 0
                else:
                    assert f"Couldn't map n={n}"
            if len(n) == 5:
                missing_letters = set(reverse_value_map[8]) - set(n)
                assert len(missing_letters) == 2, len(missing_letters)
                segment1, segment2 = missing_letters.pop(), missing_letters.pop()
                if all((segment1 in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                    if not any((segment2 in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                        value_map[n] = 5
                    else:
                        assert segment1 in reverse_value_map[4]
                        assert segment2 in reverse_value_map[4]
                        # Should be a sufficient sanity check imo
                        value_map[n] = 2
                elif all((segment2 in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                    if not any((segment1 in disp) for disp in  map(reverse_value_map.get, (1,4,7))):
                        value_map[n] = 5
                    else:
                        assert segment1 in reverse_value_map[4]
                        assert segment2 in reverse_value_map[4]
                        # Should be a sufficient sanity check imo
                        value_map[n] = 2
                else:
                    assert(
                        not any((segment1 in disp) for disp in map(reverse_value_map.get, (1,4,7)))
                        or
                        not any((segment2 in disp) for disp in map(reverse_value_map.get, (1,4,7)))
                    )
                    value_map[n] = 3
        output = 0
        for idx, n in enumerate(self.output_value):
            n = "".join(sorted(n))
            output = 10 * output + value_map[n]
        return output





    @staticmethod
    def parse(signal_line:str):
        return Signal(*map(methodcaller("split", " "), signal_line.split(" | ")))

total_output = 0
signals = map(Signal.parse, puzzle_input)
# total_output = sum(map(methodcaller("decode"), signals))
for x in map(methodcaller("decode"), signals):
    print(x)
    total_output += x
# Result
print(total_output)