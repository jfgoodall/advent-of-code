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
    vx, vy = vel
    x, y = 0, 0
    max_height = y
    while True:
        max_height = max(max_height, y)
        if target[0][0] <= x <= target[0][1] and target[1][0] <= y <= target[1][1]:
            return max_height
        if x > target[0][1] or y < target[1][0]:
            return None
        x += vx
        y += vy
        vx = max(0, vx-1)
        vy -= 1

def part1(target):
    max_h = target[1][0]
    for vy in range(target[1][0], 500):
        for vx in range(1, target[0][1]+1):
            h = max_height((vx, vy), target)
            if h is not None:
                max_h = max(max_h, h)
    return max_h

def part2(target):
    valid_count = 0
    for vy in range(target[1][0], 500):
        for vx in range(1, target[0][1]+1):
            if max_height((vx, vy), target) is not None:
                valid_count += 1
    return valid_count

def parse_input(data_src):
    data_src.seek(0)
    match = re.match(r'target area: x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)',
                     next(data_src).strip())
    vals = list(map(int, match.groups()))
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
