#!/usr/bin/env python3
from io import StringIO
import numpy as np
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def accumulate(vectors):
    cumvec = np.zeros(3, dtype=int)  # (forward, aim, depth)
    for step in vectors:
        cumvec += (step[0], step[1], step[0]*cumvec[1])
    return cumvec

def part1(vectors):
    cumvec = accumulate(vectors)
    return cumvec[0] * cumvec[1]

def part2(vectors):
    cumvec = accumulate(vectors)
    return cumvec[0] * cumvec[2]

def parse_input(data_src):
    inp = data_src.readlines()

    DIRECTION_MAP = {'forward': np.array((1, 0)),
                     'up': np.array((0, -1)),
                     'down': np.array((0, 1))}
    return [DIRECTION_MAP[x[0]]*int(x[1]) for x in
            (line.split() for line in inp)]

def run_tests():
    TEST_INPUT = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 150
    assert part2(parsed) == 900

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 1936494
    print(f"Part 2: {part2(parsed)}")  # 1997106066
