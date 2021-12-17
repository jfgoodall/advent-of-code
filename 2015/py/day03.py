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

DIR_MAP = {'^': (0, 1), 'v': (0, -1), '<': (-1, 0), '>': (1, 0)}

def part1(data):
    count = 0
    for line in data:
        here = np.zeros(2, dtype=int)
        delivered = set()
        delivered.add(tuple(here))
        for direction in line:
            here += DIR_MAP[direction]
            delivered.add(tuple(here))
        count += len(delivered)
    return count

def part2(data):
    count = 0
    for line in data:
        here = np.zeros((2, 2), dtype=int)
        delivered = set()
        delivered.add(tuple(here[0]))
        for direction in line:
            here[0] += DIR_MAP[direction]
            delivered.add(tuple(here[0]))
            here = np.flip(here, axis=0)
        count += len(delivered)
    return count

def parse_input(data_src):
    data_src.seek(0)
    return [line.strip() for line in data_src]

def run_tests():
    TEST_INPUT = """
>
^>v<
^v^v^v^v^v
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 8
    TEST_INPUT = """
^v
^>v<
^v^v^v^v^v
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part2(parse_input(test_data)) == 17

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 2592
        print_result('2', part2, parse_input(infile))  # 2360
