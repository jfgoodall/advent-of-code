#!/usr/bin/env python3
import time
from io import StringIO


def part1(calories):
    return max(calories)

def part2(calories):
    return sum(sorted(calories)[-3:])

def parse_input(data_src):
    data_src.seek(0)
    calories = [0]
    for line in data_src:
        line = line.strip()
        if line:
            calories[-1] += int(line)
        else:
            calories.append(0)
    return calories

def run_tests():
    TEST_INPUT = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 24000
    assert part2(parse_input(test_data)) == 45000

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 74711
        print_result('2', part2, parse_input(infile))  # 209481
