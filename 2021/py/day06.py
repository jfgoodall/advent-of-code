#!/usr/bin/env python3
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable
from collections import Counter


def part1(fish, days=80):
    for _ in range(days):
        next_gen = Counter()
        for timer, count in fish.items():
            if timer:
                next_gen[timer-1] += count
            else:
                next_gen[6] += count
                next_gen[8] += count
        fish = next_gen
    return sum(fish.values())

def part2(fish):
    return part1(fish, days=256)

def parse_input(data_src):
    inp = data_src.readlines()
    assert len(inp) == 1
    return Counter(map(int, inp[0].split(',')))

def run_tests():
    TEST_INPUT = """
3,4,3,1,2
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed.copy()) == 5934
    assert part2(parsed.copy()) == 26984457539

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 372984
    print(f"Part 2: {part2(parsed)}")  # 1681503251694
