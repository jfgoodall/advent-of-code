#!/usr/bin/env python3
import functools
import itertools
import re
import time
from collections import Counter, defaultdict
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(parsed):
    pass

def part2(parsed):
    pass

def parse_input(data_src):
    data_src.seek(0)
    for line in data_src:
        pass
    return parsed

def run_tests():
    TEST_INPUT = """
test data
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 0
    assert part2(parse_input(test_data)) == 0

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # -
        print_result('2', part2, parse_input(infile))  # -
