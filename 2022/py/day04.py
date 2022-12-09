#!/usr/bin/env python3
import re
import time
from io import StringIO


def fully_contains(a, b):
    return a[0] <= b[0] and a[1] >= b[1] or b[0] <= a[0] and b[1] >= a[1]

def ranges_overlap(a, b):
    return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]

def part1(assignments):
    return sum(fully_contains(*sections) for sections in assignments)

def part2(assignments):
    return sum(ranges_overlap(*sections) for sections in assignments)

def parse_input(data_src):
    data_src.seek(0)
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    assignments = []
    for line in data_src:
        a, b, c, d = map(int, pattern.match(line).groups())
        assignments.append(((a, b), (c, d)))
    return assignments

def run_tests():
    TEST_INPUT = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 2
    assert part2(parse_input(test_data)) == 4

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 513
        print_result('2', part2, parse_input(infile))  # 878
