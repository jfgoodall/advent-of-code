#!/usr/bin/env python3
from io import StringIO
import numpy as np
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def define_grid(segments):
    max_dim = segments.max()+1
    return np.zeros((max_dim, max_dim))

def plot_points(grid, segments, diagonal: bool):
    for p1, p2 in segments:
        if p1[0] == p2[0]:
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            for y in range(p1[1], p2[1]+1):
                grid[y,p1[0]] += 1
        elif p1[1] == p2[1]:
            if p1[0] > p2[0]:
                p1, p2 = p2, p1
            for x in range(p1[0], p2[0]+1):
                grid[p1[1],x] += 1
        elif diagonal:
            if p1[0] > p2[0]:
                p1, p2 = p2, p1
            y_inc = 1 if p1[1] < p2[1] else -1
            y = p1[1]
            for x in range(p1[0], p2[0]+1):
                grid[y,x] += 1
                y += y_inc

def part1(segments):
    grid = define_grid(segments)
    plot_points(grid, segments, diagonal=False)
    return (grid>1).sum()

def part2(segments):
    grid = define_grid(segments)
    plot_points(grid, segments, diagonal=True)
    return (grid>1).sum()

def parse_input(data_src):
    inp = data_src.readlines()
    segments = []
    for line in inp:
        tokens = line.split()
        p1 = tokens[0].split(',')
        p2 = tokens[2].split(',')
        segments.append(((int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))))
    return np.asarray(segments)

def run_tests():
    TEST_INPUT = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 5
    assert part2(parsed) == 12

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 6666
    print(f"Part 2: {part2(parsed)}")  # 19081
