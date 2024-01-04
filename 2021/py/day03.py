#!/usr/bin/env python3
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable
from collections import Counter
from functools import partial


def part1(data, nbits):
    bit_counts = Counter()
    for value in data:
        for bit in range(nbits):
            mask = 1 << bit
            bit_counts[bit] += (value & mask) >> bit

    gamma = 0
    for bit in range(nbits):
        if bit_counts[bit] > len(data)//2:
            gamma |= 1 << bit
    epsilon = gamma ^ ((1<<nbits)-1)

    return gamma * epsilon

def part2(data, nbits):
    majority = len(data) // 2
    oxy_data = data.copy()
    for bit in reversed(range(nbits)):
        majority = len(oxy_data) / 2
        bit_count = sum(bool((1<<bit)&x) for x in oxy_data)

        mask = 1 << bit
        oxy_data = list(
                filter(lambda x: ((x&mask)>>bit) == (bit_count>=majority),
                       oxy_data))
        if len(oxy_data) == 1:
            break

    c02_data = data
    for bit in reversed(range(nbits)):
        majority = len(c02_data) / 2
        bit_count = sum(bool((1<<bit)&x) for x in c02_data)

        mask = 1 << bit
        c02_data = list(
                filter(lambda x: ((x&mask)>>bit) == (bit_count<majority),
                       c02_data))
        if len(c02_data) == 1:
            break

    return oxy_data[0] * c02_data[0]

def parse_input(data_src):
    inp = data_src.readlines()
    return list(map(partial(int, base=2), inp))

def run_tests():
    TEST_INPUT = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed, 5) == 198
    assert part2(parsed, 5) == 230

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed, 12)}")  # 4006064
    print(f"Part 2: {part2(parsed, 12)}")  # 5941884
