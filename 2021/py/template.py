#!/usr/bin/env python3
import itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
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
    with StringIO(TEST_INPUT.strip()) as test_data:
        assert part1(parse_input(test_data)) == 0
        # assert part2(parse_input(test_data)) == 0

if __name__ == '__main__':
    run_tests()
    # with open(__file__[:-3] + '-input.dat') as infile:
    #     print(f"Part 1: {part1(parse_input(infile))}")  # 4411
    #     print(f"Part 2: {part2(parse_input(infile))}")  # 136767
