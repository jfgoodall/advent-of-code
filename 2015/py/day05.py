#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(lines):
    return sum(len(re.findall(r'[aeiou]', line)) >= 3 and
               len(re.findall(r'(.)\1', line)) > 0 and
               len(re.findall(r'(ab)|(cd)|(pq)|(xy)', line)) == 0
               for line in lines)

def part2(lines):
    return sum(len(re.findall(r'(..).*\1', line)) > 0 and
               len(re.findall(r'(.).\1', line)) > 0
               for line in lines)

def parse_input(data_src):
    data_src.seek(0)
    return [line.strip() for line in data_src]

def run_tests():
    TEST_INPUT = """
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 2

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 255
        print_result('2', part2, parse_input(infile))  # 55
