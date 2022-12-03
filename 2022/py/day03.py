#!/usr/bin/env python3
import string
import time
from io import StringIO

PRIORITY = {c: v for v, c in
                enumerate(string.ascii_lowercase + string.ascii_uppercase, 1)}

def part1(sacks):
    total = 0
    for sack in sacks:
        l = len(sack) // 2
        common = (set(sack[:l]) & set(sack[l:])).pop()
        total += PRIORITY[common]
    return total

def part2(sacks):
    total = 0
    for i in range(len(sacks) // 3):
        common = set(sacks[i*3]) & set(sacks[i*3+1]) & set(sacks[i*3+2])
        total += PRIORITY[common.pop()]

    # alt version:
    # it = iter(sacks)
    # while groups := list(itertools.islice(it, 3)):
    #     common = functools.reduce(operator.and_, map(set, groups))
    #     total += PRIORITY[common.pop()]

    return total

def parse_input(data_src):
    data_src.seek(0)
    return [line.strip() for line in data_src]

def run_tests():
    TEST_INPUT = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 157
    assert part2(parse_input(test_data)) == 70

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 7821
        print_result('2', part2, parse_input(infile))  # 2752
