#!/usr/bin/env python3
import itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def power_up(grid, row, col):
    if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
        grid[row, col] += 1
        if grid[row, col] == 10:
            return (power_up(grid, row-1, col-1) + power_up(grid, row-1, col) +
                    power_up(grid, row-1, col+1) + power_up(grid, row, col-1) +
                    power_up(grid, row, col+1) + power_up(grid, row+1, col-1) +
                    power_up(grid, row+1, col) + power_up(grid, row+1, col+1) + 1)
    return 0

def part1(grid):
    flashes = 0
    for _ in range(100):
        flashes += sum(power_up(grid, *idx) for idx in np.ndindex(grid.shape))
        grid = np.where(grid>9, 0, grid)
    return flashes

def part2(grid):
    for step in itertools.count(start=1):
        for idx in np.ndindex(grid.shape):
            power_up(grid, *idx)
        if np.all(grid > 9):
            return step
        grid = np.where(grid>9, 0, grid)

def parse_input(data_src):
    lines = data_src.readlines()
    num_rows = len(lines)
    nums = list(''.join(line.strip() for line in lines))
    return np.array(list(map(int, nums))).reshape(num_rows, -1)

def run_tests():
    TEST_INPUT = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed.copy()) == 1656
    assert part2(parsed.copy()) == 195

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed.copy())}")  # 1615
    print(f"Part 2: {part2(parsed.copy())}")  # 249
