#!/usr/bin/env python3
import math
import time
from io import StringIO


def solve_quadratic(time, dist):
    # -t^2 + time*t - dist > 0
    a = -1
    b = time
    c = -dist
    discr = b*b - 4*a*c
    assert discr > 0
    x = (-b + discr**0.5) / (2*a)
    y = (-b - discr**0.5) / (2*a)

    # account for the inequality
    x = math.nextafter(x, x+1)
    y = math.nextafter(y, y-1)

    return math.floor(y) - math.ceil(x) + 1

def part1(pairs, *_):
    return math.prod(solve_quadratic(t, d) for t, d in pairs)

def part1_incremental(pairs, *_):
    total = 1
    for time, dist in pairs:
        ways = 0
        for t in range(1, time):
            if t * (time-t) > dist:
                ways += 1
        total *= ways
    return total

def part2(_, time, dist):
    return solve_quadratic(time, dist)

def part2_binary_search(_, time, dist):
    # binary search approach assumes time/2 is a winning time
    low, high = 0, time
    while high-low > 1:
        t = low + (high - low) // 2
        if t * (time-t) > dist:
            high = t
        else:
            low = t
    start = high

    low, high = 0, time
    while high-low > 1:
        t = low + (high - low) // 2
        if t * (time-t) < dist:
            high = t
        else:
            low = t
    end = high

    return end - start

def parse_input(data_src):
    data_src.seek(0)
    t = data_src.readline().split(':')[1]
    d = data_src.readline().split(':')[1]
    pairs = zip(map(int, t.split()), map(int, d.split()))
    time = int(''.join(t.split()))
    dist = int(''.join(d.split()))
    return [list(pairs), time, dist]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 1159152

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 41513103

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (288, 71503)
    TEST_INPUT = """
Time:      7  15   30
Distance:  9  40  200
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
