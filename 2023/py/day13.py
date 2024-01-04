#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np


def mirror_value(pattern, smudge=False):
    for row in range(1, pattern.shape[0]):
        top = pattern[:row]
        bottom = pattern[row:]
        rows = min(top.shape[0], bottom.shape[0])
        top = top[-rows:]
        bottom = bottom[:rows]
        if np.sum(~(top == np.flip(bottom, axis=0))) == smudge:
            return 100*row

    for col in range(1, pattern.shape[1]):
        left = pattern[:,:col]
        right = pattern[:,col:]
        cols = min(left.shape[1], right.shape[1])
        left = left[:,-cols:]
        right = right[:,:cols]
        if np.sum(~(left == np.flip(right, axis=1))) == smudge:
            return col

    assert False

def part1(patterns):
    return sum(mirror_value(p) for p in patterns)

def part2(patterns):
    return sum(mirror_value(p, smudge=True) for p in patterns)

def parse_input(data_src):
    data_src.seek(0)
    patterns = []
    for pattern in data_src.read().split('\n\n'):
        pattern = pattern.splitlines()
        arr = np.chararray((len(pattern), len(pattern[0])))
        for i, line in enumerate(pattern):
            arr[i] = list(line)
        patterns.append(arr)
    return [patterns]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 35691

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 39037

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (405, 400)
    TEST_INPUT = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
