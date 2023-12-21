#!/usr/bin/env python3
import heapq
import time
from collections import defaultdict
from io import StringIO

import numpy as np
import tqdm


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

def dijkstra(graph, start, show_progress=False):
    heap = []
    coord_map = {}

    s = set(x[0] for m in graph.values() for x in m)
    with tqdm.tqdm(total=len(s)-1, disable=not show_progress) as pbar:
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
                    pbar.update()

    return coord_map

def part1(garden, start, steps=64):
    graph = grid_to_graph(garden)
    coord_map = dijkstra(graph, start)

    PARITY = steps % 2
    count = 0
    for node in coord_map.values():
        if node.dist <= steps and node.dist%2 == PARITY:
            count += 1
    return count

def part2(garden, start):
    """this only works because there are no rocks through the center of the __real__ data
       (the test data is garbage here) and because:
           (26501365-garden.shape//2)%garden.shape == 0
       puzzles where the solution can only be found by analyzing the specific input data
       rather than the puzzle description and example data kinda suck"""
    # show partitioning by parity
    # start_parity = (start[0]+start[1]) % 2
    # plots = 0
    # reachable = 0
    # for idx, val in np.ndenumerate(garden):
    #     if val == '.':
    #         plots += 1
    #         if (idx[0]+idx[1])%2 == start_parity:
    #             reachable += 1
    # parity0 = reachable
    # parity1 = plots - reachable
    # print(f'{parity0=} {parity1=}')

    # tile the garden into a 5x5 configuration to make sure we have both "parity" cases
    # covered in all directions from the center
    spread = 2
    tile_size = garden.shape[0]
    start = (start[0]+tile_size*spread, start[1]+tile_size*spread)
    garden = np.tile(garden, (spread*2+1, spread*2+1))

    # part 1 on the tiled garden
    graph = grid_to_graph(garden)
    coord_map = dijkstra(graph, start, show_progress=True)

    # find number of plots reachable in step counts that reach the end of a tiling period
    targets = np.array([tile_size//2+tile_size*x for x in range(spread+1)])
    plots = np.zeros(len(targets))
    for node in tqdm.tqdm(coord_map.values()):
        for idx, target in enumerate(targets):
            if node.dist <= target and node.dist%2 == target%2:
                plots[idx] += 1

    # works but result is too big by 0.6 due to precision
    # coeffs = np.polynomial.polynomial.polyfit(targets, plots, deg=2)
    # poly = np.polynomial.Polynomial(coeffs)
    # return poly(26501365)

    # better interpolation compatible with float128
    import scipy.interpolate
    poly = scipy.interpolate.lagrange(targets.astype(np.longdouble), plots.astype(np.longdouble))
    return poly(26501365)

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    garden = np.array([list(l) for l in lines])
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

        # assert part2(*parse_input(test_data), steps=50) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 621289922886149

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
