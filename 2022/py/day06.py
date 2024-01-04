#!/usr/bin/env python3
import time
from io import StringIO


def find_marker(signal, num_unique):
    for i in range(num_unique, len(signal)):
        if len(set(signal[i-num_unique:i])) == num_unique:
            return i

def part1(signal):
    return find_marker(signal, 4)

def part2(signal):
    return find_marker(signal, 14)

def parse_input(data_src):
    data_src.seek(0)
    return data_src.read().strip()

def run_tests():
    TEST_INPUT = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 7
    assert part2(parse_input(test_data)) == 19

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 1850
        print_result('2', part2, parse_input(infile))  # 2823
