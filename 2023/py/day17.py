#!/usr/bin/env python3
import heapq
import time
from io import StringIO

import numpy as np


def find_min_dist(grid, max_run, min_run=1):
    target = (grid.shape[0]-1, grid.shape[1]-1)
    visited = set()
    heap = []

    heapq.heappush(heap, (grid[0,1], (0, 1), (0, 1), 1))
    heapq.heappush(heap, (grid[1,0], (1, 0), (1, 0), 1))

    while heap:
        dist, pos, direction, run = heapq.heappop(heap)
        if pos == target and run >= min_run:
            return dist
        if (pos, direction, run) in visited:
            continue
        visited.add((pos, direction, run))

        if run < max_run:
            # go straight
            new_pos = (pos[0]+direction[0], pos[1]+direction[1])
            if 0 <= new_pos[0] < grid.shape[0] and 0 <= new_pos[1] < grid.shape[1]:
                heapq.heappush(heap, (dist+grid[new_pos], new_pos, direction, run+1))

        if run >= min_run:
            # turn right
            new_dir = (direction[1], -direction[0])
            new_pos = (pos[0]+new_dir[0], pos[1]+new_dir[1])
            if 0 <= new_pos[0] < grid.shape[0] and 0 <= new_pos[1] < grid.shape[1]:
                heapq.heappush(heap, (dist+grid[new_pos], new_pos, new_dir, 1))

            # turn left
            new_dir = (-direction[1], direction[0])
            new_pos = (pos[0]+new_dir[0], pos[1]+new_dir[1])
            if 0 <= new_pos[0] < grid.shape[0] and 0 <= new_pos[1] < grid.shape[1]:
                heapq.heappush(heap, (dist+grid[new_pos], new_pos, new_dir, 1))

def part1(grid):
    return find_min_dist(grid, 3)

def part2(grid):
    return find_min_dist(grid, 10, 4)

def parse_input(data_src):
    data_src.seek(0)
    grid = []
    for line in data_src:
        grid.append(list(map(int, list(line.strip()))))
    return [np.array(grid, dtype=int)]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 1039

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 1201

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (102, 94)
    TEST_INPUT = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
