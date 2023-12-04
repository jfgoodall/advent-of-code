#!/usr/bin/env python3
import time
from functools import lru_cache
from io import StringIO


def part1(matches):
    return sum(2**(m-1) if m else 0 for m in matches)

def part2(matches):
    @lru_cache(maxsize=None)
    def get_bonus_cards(idx):
        return 1 + sum(get_bonus_cards(i) for i in range(idx+1, idx+matches[idx]+1))

    return sum(get_bonus_cards(i) for i in range(len(matches)))

def parse_input(data_src):
    data_src.seek(0)
    matches = []
    for line in data_src.read().splitlines():
        nums = line.split(':')[1].split('|')
        matched_nums = set(map(int, nums[0].split())) & set(map(int, nums[1].split()))
        matches.append(len(matched_nums))
    return [matches]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 28750

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 10212704

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (13, 30)
    TEST_INPUT = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
