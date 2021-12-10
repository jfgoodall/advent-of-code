#!/usr/bin/env python3
from io import StringIO
import numpy as np
from collections import Counter
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def get_neighbors(grid, row, col):
    neighbors = []
    if row > 0:
        neighbors.append((row-1, col, grid[row-1, col]))
    if row < grid.shape[0]-1:
        neighbors.append((row+1, col, grid[row+1, col]))
    if col > 0:
        neighbors.append((row, col-1, grid[row, col-1]))
    if col < grid.shape[1]-1:
        neighbors.append((row, col+1, grid[row, col+1]))
    return neighbors  # list of (row, col, val)

def part1(grid):
    total = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            neighbors = get_neighbors(grid, row, col)
            if all(grid[row, col] < n[2] for n in neighbors):
                total += grid[row, col] + 1
    return total

def fill_basin(grid, row, col, val):
    grid[row, col] = val
    neighbors = get_neighbors(grid, row, col)
    for n in neighbors:
        if n[2] == 0:
            fill_basin(grid, n[0], n[1], val)

def part2(grid):
    grid = np.vectorize(lambda x: -1 if x==9 else 0)(grid)

    basin_val = 1
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 0:
                fill_basin(grid, row, col, basin_val)
                basin_val += 1

    basins = Counter(grid.reshape(-1,))
    basins.pop(-1)
    sizes = sorted(basins.values())
    return sizes[-1] * sizes[-2] * sizes[-3]

def parse_input(data_src):
    inp = data_src.readlines()
    grid = np.empty((len(inp), len(inp[0])-1), dtype=int)
    for row, line in enumerate(inp):
        grid[row] = [int(height) for height in line.strip()]
    return grid

def run_tests():
    TEST_INPUT = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 15
    assert part2(parsed) == 1134

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 425
    print(f"Part 2: {part2(parsed)}")  # 1135260
