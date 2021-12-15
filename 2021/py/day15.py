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

def traverse(grid, coord, seen, risk, best):
    if coord in seen or coord[0] < 0 or coord[0] >= grid.shape[0] or coord[1] < 0 or coord[1] >= grid.shape[1]:
        return best

    if sum(x in seen for x in ((coord[0]-1, coord[1]),
                               (coord[0]+1, coord[1]),
                               (coord[0], coord[1]-1),
                               (coord[0], coord[1]+1))) > 1:
        return best

    if grid.shape[0]-coord[0]-1 + grid.shape[1]-coord[1]-1 > best-risk:
        return risk

    risk += grid[coord]
    if risk >= best:
        return best

    if (coord[0]+1, coord[1]+1) == grid.shape:
        # g = np.zeros(grid.shape, dtype=int)
        # for c in seen:
        #     g[c] = 1
        # print(g)
        return min(risk, best)

    seen.add(coord)
    # up = traverse(grid, (coord[0]-1, coord[1]), seen.copy(), risk, best)
    down = traverse(grid, (coord[0]+1, coord[1]), seen.copy(), risk, best)
    # left = traverse(grid, (coord[0], coord[1]-1), seen.copy(), risk, best)
    right = traverse(grid, (coord[0], coord[1]+1), seen.copy(), risk, best)
    # return min(up, down, left, right)
    return min(down, right)

def part1_(grid):
    # grid = grid[:10,:9]
    print(grid)
    best = grid[0,:].sum() + grid[:,-1].sum() - grid[0,-1] - grid[0,0]
    print(best)
    # print(traverse(grid, (0, 0), set(), -grid[0,0], best))
    return traverse(grid, (0, 0), set(), -grid[0,0], best)

def part1(grid):
    print(grid)
    grid[0,1:] = np.cumsum(grid[0,1:])
    grid[1:,0] = np.cumsum(grid[1:,0])
    for row in range(1, grid.shape[0]):
        for col in range(1, grid.shape[1]):
            grid[row, col] += min(grid[row-1, col], grid[row, col-1])
    print(grid)
    return grid[-1,-1]

def part2(parsed):
    pass

def parse_input(data_src):
    data_src.seek(0)
    grid = []
    for line in data_src:
        grid.append(list(map(int, list(line.strip()))))
    return np.asarray(grid, dtype=int)

def run_tests():
    TEST_INPUT = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 40
    # assert part2(parse_input(test_data)) == 0
    print('--passed tests--')

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 685 ????
    #     print_result('2', part2, parse_input(infile))  # -
