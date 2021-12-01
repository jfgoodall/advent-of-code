#!/usr/bin/env python3
from io import StringIO
import numpy as np
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1():
    pass

def part2():
    pass

def parse_input(data_src):
    inp = data_src.readlines()

    return parsed

def run_tests():
    TEST_INPUT = """
test
data
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    # assert part1(parsed) == 165

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # <ans>
    print(f"Part 2: {part2(parsed)}")  # <ans>
