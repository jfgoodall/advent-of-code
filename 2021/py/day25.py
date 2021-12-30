#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

EMPTY = 0
EAST = 1
SOUTH = 3  # don't use 2

def dump_grid(grid, msg=None):
    if msg:
        print(msg)
    for row in grid:
        for col in row:
            print('.' if col==0 else '>' if col==EAST else 'v', end='')
        print()
    print()

def step_grid(grid, direction):
    padded = np.pad(grid, ((0, 1), (0, 0)), 'wrap')
    movable = grid - padded[1:,] == direction
    padded[:-1,][movable] = 0
    padded[-1,][movable[0,]] = 0  # maintain wrapped row (tail)
    padded[1:,][movable] = direction
    padded[0,] = padded[-1,]  # maintain wrapped row (head)
    return padded[:-1,]

def part1(grid):
    for i in itertools.count(1):
        stepped = step_grid(grid.T, EAST).T
        stepped = step_grid(stepped, SOUTH)
        if np.all(stepped == grid):
            return i
        grid = stepped

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.readlines()
    grid = np.empty((len(lines), len(lines[0].strip())))
    for row, line in enumerate(lines):
        for col, val in enumerate(line.strip()):
            grid[row,col] = 0 if val == '.' else EAST if val == '>' else SOUTH
    return grid

def run_tests():
    TEST_INPUT = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 58

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 424
