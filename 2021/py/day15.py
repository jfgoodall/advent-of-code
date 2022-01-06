#!/usr/bin/env python3
import functools
import heapq
import time
from collections import defaultdict
from io import StringIO

import numpy as np

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
    return graph  # {coord: {(neighbor_coord, distance)}

def bigify_grid(grid):
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
    return big

def dijkstra(graph, target):
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

    add_node((0, 0), 0)
    while heap:
        current = heapq.heappop(heap)
        if current.removed:
            continue
        if current.coord == target:
            break
        for neighbor, dist in graph[current.coord]:
            if neighbor in coord_map:
                if current.dist+dist < coord_map[neighbor].dist:
                    coord_map[neighbor].removed = True
                    add_node(neighbor, current.dist+dist)
            else:
                add_node(neighbor, current.dist+dist)

    return coord_map[target].dist

def a_star(graph, target):
    class Node:
        __slots__ = 'coord', 'dist', 'fscore', 'removed'
        def __init__(self, coord, dist):
            self.coord = coord
            self.dist = dist
            self.fscore = dist + target[0]-coord[0] + target[1]-coord[1]
            self.removed = False
        def __lt__(self, other):
            return self.fscore < other.fscore

    heap = []
    coord_map = {}

    def add_node(coord, dist):
        node = Node(coord, dist)
        coord_map[coord] = node
        heapq.heappush(heap, node)

    add_node((0, 0), 0)
    while heap:
        current = heapq.heappop(heap)
        if current.removed:
            continue
        if current.coord == target:
            break
        for neighbor, dist in graph[current.coord]:
            if neighbor in coord_map:
                if current.dist+dist < coord_map[neighbor].dist:
                    coord_map[neighbor].removed = True
                    add_node(neighbor, current.dist+dist)
            else:
                add_node(neighbor, current.dist+dist)

    return coord_map[target].dist

def part1(algo, grid):
    graph = grid_to_graph(grid)
    target = (grid.shape[0]-1, grid.shape[1]-1)
    return algo(graph, target)

def part2(algo, grid):
    grid = bigify_grid(grid)
    graph = grid_to_graph(grid)
    target = (grid.shape[0]-1, grid.shape[1]-1)
    return algo(graph, target)

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
    assert part1(dijkstra, parse_input(test_data)) == 40
    assert part1(a_star, parse_input(test_data)) == 40
    assert part2(dijkstra, parse_input(test_data)) == 315
    assert part2(a_star, parse_input(test_data)) == 315

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1 Dijkstra', functools.partial(part1, dijkstra),
                     parse_input(infile))  # 685
        print_result('1 A*      ', functools.partial(part1, a_star),
                     parse_input(infile))  # 685
        print_result('2 Dijkstra', functools.partial(part2, dijkstra),
                     parse_input(infile))  # 2995
        print_result('2 A*      ', functools.partial(part2, a_star),
                     parse_input(infile))  # 2995
