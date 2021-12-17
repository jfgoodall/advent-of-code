#!/usr/bin/env python3
import time, itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(parsed):
    c = Counter(parsed)
    return c['('] - c[')']

def part2(parsed):
    DIRECTION = {'(': 1, ')': -1}
    floor = 0
    for idx, direction in enumerate(parsed, 1):
        floor += DIRECTION[direction]
        if floor == -1:
            return idx

def parse_input(data_src):
    data_src.seek(0)
    return next(data_src).strip()

def run_tests():
    TEST_INPUT = """
((()))
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 0

    TEST_INPUT = """
())
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part2(parse_input(test_data)) == 3

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 138
        print_result('2', part2, parse_input(infile))  # 1771
