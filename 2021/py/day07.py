#!/usr/bin/env python3
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(crabs, cost_fn=lambda x: x):
    return min(sum(cost_fn(abs(pos-crab)) for crab in crabs)
               for pos in range(min(crabs), max(crabs)+1))

def part2(crabs):
    return part1(crabs, lambda x: x*(x+1)//2)

def parse_input(data_src):
    inp = data_src.readlines()
    return list(map(int, inp[0].split(',')))

def run_tests():
    TEST_INPUT = """
16,1,2,0,4,2,7,1,2,14
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 37
    assert part2(parsed) == 168

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 348664
    print(f"Part 2: {part2(parsed)}")  # 100220525
