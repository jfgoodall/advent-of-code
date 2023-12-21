#!/usr/bin/env python3
import heapq
import time
from collections import defaultdict
from io import StringIO

import numpy as np


def grid_to_graph(grid):
    def valid_move(start, pt):
        if (pt[0] < 0 or pt[0] >= grid.shape[0] or pt[1] < 0 or pt[1] >= grid.shape[1]):
            return False
        return grid[pt] == '.'

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

class Node:
    __slots__ = 'coord', 'dist'
    def __init__(self, coord, dist):
        self.coord = coord
        self.dist = dist
    def __lt__(self, other):
        return self.dist < other.dist
    def __repr__(self):
        return f"{self.coord=} {self.dist=}"

def dijkstra(graph, start):
    heap = []
    coord_map = {}

    coord_map[start] = Node(start, 0)
    heapq.heappush(heap, coord_map[start])
    while heap:
        current = heapq.heappop(heap)
        for neighbor, dist in graph[current.coord]:
            if neighbor in coord_map:
                if current.dist+dist < coord_map[neighbor].dist:
                    coord_map[neighbor] = Node(neighbor, current.dist+dist)
            else:
                coord_map[neighbor] = Node(neighbor, current.dist+dist)
                heapq.heappush(heap, coord_map[neighbor])
    return coord_map

def part1(garden, start, steps=64):
    graph = grid_to_graph(garden)
    coord_map = dijkstra(graph, start)

    count = 0
    for node in coord_map.values():
        if node.dist <= steps and node.dist%2 == steps%2:
            count += 1
            garden[*node.coord] = 'O'
    return count

def part2(garden, start, steps=26501365):
    graph = grid_to_graph(garden)
    coord_map = dijkstra(graph, start)

    start_parity = (start[0]+start[1]) % 2
    plots = 0
    reachable = 0
    for idx, val in np.ndenumerate(garden):
        if val == '.':
            plots += 1
            if (idx[0]+idx[1])%2 == start_parity:
                reachable += 1
    print(f'{plots=} {reachable=} other={plots-reachable}')

    for node in coord_map.values():
        garden[*node.coord] = f'{node.dist:02}'
    for idx, val in np.ndenumerate(garden):
        if len(val) == 1:
            garden[idx] = ' '+val
    print(garden)


def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    garden = np.array([list(l) for l in lines], dtype=np.dtype('U4'))
    for (row, col), val in np.ndenumerate(garden):
        if val == 'S':
            garden[row, col] = '.'
            break
    return [garden, (row, col)]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data), steps=6) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 3729

        assert part2(*parse_input(test_data), steps=50) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (16, 1594)
    TEST_INPUT = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
