#!/usr/bin/env python3
import time, itertools, functools, heapq
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def grid_to_graph(grid):
    graph = defaultdict(set)
    for c in np.ndindex(grid.shape):
        if c[0] > 0:
            n = (c[0]-1, c[1])
            graph[c].add((n, grid[n]))
        if c[0] < grid.shape[0]-1:
            n = (c[0]+1, c[1])
            graph[c].add((n, grid[n]))
        if c[1] > 0:
            n = (c[0], c[1]-1)
            graph[c].add((n, grid[n]))
        if c[1] < grid.shape[1]-1:
            n = (c[0], c[1]+1)
            graph[c].add((n, grid[n]))
    return graph

def dijkstra(graph, target):
    max_dist = len(graph)**2 * 9

    Q = list(graph.keys())
    Q2 = set(Q)
    dist = {v: max_dist for v in Q}
    dist[(0, 0)] = 0
    prev = {v: None for v in Q}

    while Q:
        Q.sort(key=lambda x: dist[x])
        u = Q.pop(0)
        if u == target:
            break
        Q2.remove(u)
        for v, d in graph[u]:
            if v in Q2:
                alt = dist[u] + d
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return dist[target]

def part1(grid):
    graph = grid_to_graph(grid)
    target = (grid.shape[0]-1, grid.shape[1]-1)
    return dijkstra(graph, target)

def part2(grid):
    def increment_grid(g):
        return np.where(g+1>9, 1, g+1)

    big = np.empty((grid.shape[0]*5, grid.shape[1]*5), dtype=int)
    for row in range(5):
        g = grid.copy()
        for _ in range(row):
            g = increment_grid(g)
        for col in range(5):
            big[row*grid.shape[0]:(row+1)*grid.shape[0],
                col*grid.shape[1]:(col+1)*grid.shape[1]] = g
            g = increment_grid(g)
    grid = big

    graph = grid_to_graph(grid)
    target = (grid.shape[0]-1, grid.shape[1]-1)
    return dijkstra(graph, target)

def parse_input(data_src):
    data_src.seek(0)
    grid = []
    for line in data_src:
        grid.append(list(map(int, list(line.strip()))))
    return np.array(grid, dtype=int)

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
    assert part2(parse_input(test_data)) == 315

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 685
        print_result('2', part2, parse_input(infile))  # -
