#!/usr/bin/env python3
from __future__ import annotations

import itertools
import math
import time
from io import StringIO


def is_safe(diffs):
    sign = math.copysign(1, diffs[0])
    for d in diffs:
        if math.copysign(1, d) != sign or abs(d) < 1 or abs(d) > 3:
            return False
    return True

def part1(reports):
    count = 0
    for report in reports:
        diffs = [a-b for a, b in itertools.pairwise(report)]
        count += int(is_safe(diffs))
    return count

def part2(reports):
    count = 0
    for report in reports:
        for i in range(len(reports)+1):
            diffs = [a-b for a, b in itertools.pairwise(report[:i]+report[i+1:])]
            if is_safe(diffs):
                count += 1
                break
    return count

def parse_input(data_src):
    data_src.seek(0)
    reports = []
    for line in data_src.read().splitlines():
        reports.append(list(map(int, line.split())))
    return [reports]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # -

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (2, 4)
    TEST_INPUT = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
