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

def part1(presents):
    count = 0
    for dim in presents:
        dims = (dim[0]*dim[1], dim[1]*dim[2], dim[2]*dim[0])
        count += 2 * sum(dims) + min(dims)
    return count

def part2(presents):
    count = 0
    for dim in presents:
        dims = (2*dim[0]+2*dim[1], 2*dim[1]+2*dim[2], 2*dim[2]+2*dim[0])
        count += min(dims) + dim[0]*dim[1]*dim[2]
    return count

def parse_input(data_src):
    data_src.seek(0)
    return [tuple(map(int, line.strip().split('x'))) for line in data_src]

def run_tests():
    TEST_INPUT = """
2x3x4
1x1x10
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 101
    assert part2(parse_input(test_data)) == 48

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 1588178
        print_result('2', part2, parse_input(infile))  # 3783758
