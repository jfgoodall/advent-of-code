#!/usr/bin/env python3
from io import StringIO
import numpy as np
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(depths):
    diffs = [y-x for x, y in zip(depths, depths[1:])]
    return len(list(filter(lambda x: x>0, diffs)))

def part2(depths):
    windows = [sum(depths[i:i+3]) for i in range(0, len(depths)-2)]
    return part1(windows)

def parse_input(data_src):
    inp = data_src.readlines()
    return list(map(int, inp))

def run_tests():
    TEST_INPUT = """
199
200
208
210
200
207
240
269
260
263
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 7
    assert part2(parsed) == 5

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 1688
    print(f"Part 2: {part2(parsed)}")  # 1728
