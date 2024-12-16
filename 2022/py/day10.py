#!/usr/bin/env python3
import functools
import os
import sys
import time
from io import StringIO

sys.path.append(os.path.dirname(__file__))
from common_patterns.itertools import grouper


def run_cpu(increments, update_fn):
    t = 0
    x = 1
    for inc in increments:
        update_fn(t, x)
        if inc is not None:
            t += 1
            update_fn(t, x)
            x += inc
        t += 1

def part1(increments):
    def update_signal_strengths(strengths, t, x):
        if ((t+1) - 20) % 40 == 0:
            strengths.append((t+1) * x)

    strengths = []
    run_cpu(increments,
            functools.partial(update_signal_strengths, strengths))

    return sum(strengths)

def part2(increments):
    def update_crt(crt, t, x):
        crt[t] = 1 if t%40 >= x-1 and t%40 <= x+1 else 0

    crt = [0] * 240
    run_cpu(increments, functools.partial(update_crt, crt))

    rows = [''.join(u'\u25cf'*2 if pixel else '  ' for pixel in row)
            for row in grouper(crt, 40)]
    return '\n' + '\n'.join(rows) + '\n'

def parse_input(data_src):
    data_src.seek(0)
    return [None if line.strip() == 'noop' else int(line.split()[-1])
            for line in data_src]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(parse_input(test_data)) == test_answers[0]
        print_result('1', part1, parse_input(infile))  # 14720

        # part2(parse_input(test_data))
        print_result('2', part2, parse_input(infile))  # FZBPBFZF

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (13140, 0)
    TEST_INPUT = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
