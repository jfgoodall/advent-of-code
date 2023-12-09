#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np


def part1(histories):
    total = 0
    for hist in histories:
        diffs = [hist]
        while np.any(diffs[-1]):
            diffs.append(np.diff(diffs[-1]))

        for diff in diffs:
            total += diff[-1]
    return total

def part2(histories):
    total = 0
    for hist in histories:
        diffs = [hist]
        while np.any(diffs[-1]):
            diffs.append(np.diff(diffs[-1]))

        t = 0
        for diff in reversed(diffs):
            t = diff[0] - t
        total += t
    return total

def parse_input(data_src):
    data_src.seek(0)
    histories = []
    for line in data_src.read().splitlines():
        histories.append(np.fromiter(map(int, line.split()), dtype=int))
    return [histories]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 1939607039

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 1041

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (114, 2)
    TEST_INPUT = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
