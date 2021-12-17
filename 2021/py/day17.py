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

def max_height(vel, target):
    dx, dy = vel
    x, y = 0, 0
    max_height = y
    while True:
        max_height = max(max_height, y)
        if target[0][0] <= x <= target[0][1] and target[1][0] <= y <= target[1][1]:
            return max_height
        if x > target[0][1] or y < target[1][0]:
            return None
        x += dx
        y += dy
        dx = max(0, dx-1)
        dy -= 1

def find_valid_heights(target):
    heights = []
    for dy in range(target[1][0], -target[1][0]):
        for dx in range(1, target[0][1]+1):
            h = max_height((dx, dy), target)
            if h is not None:
                heights.append(h)
    return heights

def part1(target):
    return max(find_valid_heights(target))

def part2(target):
    return len(find_valid_heights(target))

def parse_input(data_src):
    data_src.seek(0)
    match = re.findall(r'x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)',
                       next(data_src).strip())[0]
    vals = list(map(int, match))
    return vals[:2], vals[2:]

def run_tests():
    TEST_INPUT = """
target area: x=20..30, y=-10..-5
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 45
    assert part2(parse_input(test_data)) == 112

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 10878
        print_result('2', part2, parse_input(infile))  # 4716
