#!/usr/bin/env python3
import itertools
import time
from io import StringIO

import numpy as np


def solve_puzzle(grid, expansion_factor):
    empty_rows = []
    for row in range(grid.shape[0]):
        if not any(grid[row]):
            empty_rows.append(row)

    empty_cols = []
    for col in range(grid.shape[1]):
        if not any(grid[:,col]):
            empty_cols.append(col)

    pts = set()
    for i, j in np.ndindex(*grid.shape):
        if grid[i,j] != 0:
            pts.add((i, j))
    pts = {(i, j) for i, j in np.ndindex(*grid.shape) if grid[i,j]}

    total = 0
    for pt1, pt2 in itertools.combinations(pts, 2):
        dist = abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1])

        a, b = min(pt1[0], pt2[0]), max(pt1[0], pt2[0])
        for row in empty_rows:
            if row > a and row < b:
                dist += expansion_factor-1
            elif row > b:
                break

        a, b = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])
        for col in empty_cols:
            if col > a and col < b:
                dist += expansion_factor-1
            elif col > b:
                break

        total += dist
    return total

def part1(grid):
    return solve_puzzle(grid, 2)

def part2(grid, expansion_factor=1_000_000):
    return solve_puzzle(grid, expansion_factor)

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    grid = np.zeros((len(lines), len(lines[0])))
    galaxy = 1
    for row, line in enumerate(lines):
        for col, pt in enumerate(line):
            if pt == '#':
                grid[row,col] = galaxy
                galaxy += 1
    return [grid]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 10313550

        assert part2(*parse_input(test_data), 10) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 611998089572

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (374, 1030)
    TEST_INPUT = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
