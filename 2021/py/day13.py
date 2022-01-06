#!/usr/bin/env python3
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def print_grid(grid):
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            print(u'\u25cf'*2 if grid[row, col] else '  ', end='')
        print()

def fold_grid(grid, fold):
    axis, crease = fold[0], int(fold[1])
    if axis == 'x':
        grid = grid.T

    top = grid[:crease, :]
    bottom = np.flip(grid[crease+1:, :], axis=0)

    padding = top.shape[0] - bottom.shape[0]
    if padding > 0:
        bottom = np.pad(bottom, ((padding, 0), (0, 0)))
    elif padding:
        top = np.pad(top, ((0, -padding), (0, 0)))
    grid = top | bottom

    if axis == 'x':
        grid = grid.T
    return grid

def part1(grid, folds):
    grid = fold_grid(grid, folds[0])
    return grid.sum()

def part2(grid, folds):
    for fold in folds:
        grid = fold_grid(grid, fold)
    print_grid(grid)

def parse_input(data_src):
    data_src.seek(0)
    pts = []
    while line := next(data_src).strip():
        pts.append(tuple(map(int, line.split(','))))
    rows = max(pts, key=lambda x:x[1])[1] + 1
    cols = max(pts, key=lambda x:x[0])[0] + 1

    grid = np.zeros((rows, cols), dtype=bool)
    for pt in pts:
        grid[pt[1], pt[0]] = True
    folds = [line.strip().split()[2].split('=') for line in data_src]

    return grid, folds

def run_tests():
    TEST_INPUT = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        assert part1(*parse_input(test_data)) == 17
        # assert part2(*parse_input(test_data)) == 0

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print(f"Part 1: {part1(*parse_input(infile))}")  # 693
        print(f"Part 2:"); part2(*parse_input(infile))  # UCLZRAZU
