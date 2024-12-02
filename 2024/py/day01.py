#!/usr/bin/env python3
import time
from collections import Counter
from io import StringIO


def part1(l1, l2):
    return sum(abs(a-b) for a, b in zip(sorted(l1), sorted(l2)))

def part2(l1, l2):
    counts = Counter(l2)
    return sum(a * counts[a] for a in l1)

def parse_input(data_src):
    data_src.seek(0)
    list1 = []
    list2 = []
    for line in data_src.read().splitlines():
        a, b = line.split()
        list1.append(int(a))
        list2.append(int(b))
    return [list1, list2]  # note: return single item as [item] for *parse_input

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
    TEST_RESULTS = [11, 31]
    TEST_INPUT = """
3   4
4   3
2   5
1   3
3   9
3   3
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
