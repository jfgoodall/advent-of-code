#!/usr/bin/env python3
from __future__ import annotations

import heapq
import string
import time
from collections import defaultdict
from io import StringIO

import numpy as np


def grid_to_graph(grid):
    def valid_move(start, pt):
        if (pt[0] < 0 or pt[0] >= grid.shape[0] or pt[1] < 0 or pt[1] >= grid.shape[1]):
            return False
        if grid[pt[0], pt[1]] == -1:
            return grid[start[0], start[1]] == string.ascii_lowercase.index('z')
        return grid[pt[0], pt[1]] - grid[start[0], start[1]] <= 1

    graph = defaultdict(set)
    for c in np.ndindex(grid.shape):
        n = (c[0]-1, c[1])
        if valid_move(c, n):
            graph[c].add((n, 1))
        n = (c[0]+1, c[1])
        if valid_move(c, n):
            graph[c].add((n, 1))
        n = (c[0], c[1]-1)
        if valid_move(c, n):
            graph[c].add((n, 1))
        n = (c[0], c[1]+1)
        if valid_move(c, n):
            graph[c].add((n, 1))
    return graph  # {coord: {(neighbor_coord, distance)}

def dijkstra(grid, graph, start):
    class Node:
        __slots__ = 'coord', 'dist', 'removed'
        def __init__(self, coord, dist):
            self.coord = coord
            self.dist = dist
            self.removed = False
        def __lt__(self, other):
            return self.dist < other.dist

    heap = []
    coord_map = {}

    def add_node(coord, dist):
        node = Node(coord, dist)
        coord_map[coord] = node
        heapq.heappush(heap, node)

    add_node((start[0], start[1]), 0)
    while heap:
        current = heapq.heappop(heap)
        if current.removed:
            continue
        if grid[current.coord] == -1:
            break
        for neighbor, dist in graph[current.coord]:
            if neighbor in coord_map:
                if current.dist+dist < coord_map[neighbor].dist:
                    coord_map[neighbor].removed = True
                    add_node(neighbor, current.dist+dist)
            else:
                add_node(neighbor, current.dist+dist)

    if grid[current.coord] != -1:
        return grid.shape[0] * grid.shape[1]  # not found, use max value
    return coord_map[current.coord].dist

def part1(grid, start):
    graph = grid_to_graph(grid)
    return dijkstra(grid, graph, start)

def part2(grid, start):
    xs, ys = np.where(grid == string.ascii_lowercase.index('a'))
    starts = [pt for pt in zip(xs, ys)] + [start]

    graph = grid_to_graph(grid)
    return min(dijkstra(grid, graph, s) for s in starts)

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    grid = np.zeros((len(lines[0]), len(lines)), dtype=int)
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == 'S':
                start = (x, y)
                grid[x,y] = string.ascii_lowercase.index('a')
            elif cell == 'E':
                grid[x,y] = -1
            else:
                grid[x,y] = string.ascii_lowercase.index(cell)
    return grid, start

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 490

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 488

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (31, 29)
    TEST_INPUT = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
