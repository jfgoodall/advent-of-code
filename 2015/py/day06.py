#!/usr/bin/env python3
import time, itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(lines):
    grid = np.zeros((1000, 1000), dtype=bool)
    for instr, p1, p2 in lines:
        window = grid[p1[0]:p2[0]+1, p1[1]:p2[1]+1]
        if instr == 'on':
            window |= np.ones(window.shape, dtype=bool)
        elif instr == 'off':
            window &= np.zeros(window.shape, dtype=bool)
        else:  # 'toggle'
            window ^= np.ones(window.shape, dtype=bool)
    return grid.sum()

def part2(lines):
    grid = np.zeros((1000, 1000), dtype=int)
    for instr, p1, p2 in lines:
        window = grid[p1[0]:p2[0]+1, p1[1]:p2[1]+1]
        if instr == 'on':
            window += 1
        elif instr == 'off':
            window -= 1
            grid = np.where(grid<0, 0, grid)
        else:  # 'toggle'
            window += 2
        assert(np.all(grid>=0))
    return grid.sum()

def parse_input(data_src):
    data_src.seek(0)
    data = []
    for line in data_src:
        words = line.split()
        data.append((
            words[1] if words[0]=='turn' else words[0],
            tuple(map(int, words[-3].split(','))),
            tuple(map(int, words[-1].split(',')))))
    return data

def run_tests():
    TEST_INPUT = """
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 1000*1000 - 1000 - 4
    # assert part2(parse_input(test_data)) == 0

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 400410
        print_result('2', part2, parse_input(infile))  # 15343601
