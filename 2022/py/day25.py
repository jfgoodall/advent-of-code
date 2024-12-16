#!/usr/bin/env python3
import time
from io import StringIO

SNAFU_MAP = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '='
}

def snafu_to_int(snafu):
    return sum(SNAFU_MAP[digit] * pow(5, power)
               for power, digit in enumerate(reversed(snafu)))

def int_to_snafu(val):
    # convert to base 5
    snafu = []
    while val:
        snafu.append(val % 5)
        val //= 5

    # fix any digits > 2
    for power, digit in enumerate(snafu):
        if digit > 2:
            if power + 1 == len(snafu):
                snafu.append(0)
            snafu[power+1] += 1
            snafu[power] = snafu[power] - 5

    return ''.join(SNAFU_MAP[digit] for digit in reversed(snafu))

def part1(fuel):
    total = sum(snafu_to_int(val) for val in fuel)
    return int_to_snafu(total)

def parse_input(data_src):
    data_src.seek(0)
    return [data_src.read().splitlines()]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 2==221=-002=0-02-000

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = ('2=-1=0',)
    TEST_INPUT = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
