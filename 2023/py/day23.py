#!/usr/bin/env python3
import time
from collections import defaultdict
from io import StringIO

import numpy as np


def part1(grid):
    edges = defaultdict(dict)
    for pt, v in np.ndenumerate(grid):
        match v:
            case ".":
                for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    adj = pt[0]+dr, pt[1]+dc
                    if (0 <= adj[0] < grid.shape[0] and
                        0 <= adj[1] < grid.shape[1] and
                        grid[adj] == "."
                    ):
                        edges[pt][adj] = 1
                        edges[adj][pt] = 1
            case ">":
                edges[pt][pt[0], pt[1]+1] = 1
                edges[pt[0], pt[1]-1][pt] = 1
            case "v":
                edges[pt][pt[0]+1, pt[1]] = 1
                edges[pt[0]-1, pt[1]][pt] = 1
            case "<":
                edges[pt][pt[0], pt[1]-1] = 1
                edges[pt[0], pt[1]+1][pt] = 1
            case "^":
                edges[pt][pt[0]-1, pt[1]] = 1
                edges[pt[0]+1, pt[1]][pt] = 1

    # combine non-branching edges
    while True:
        for node, connected in edges.items():
            if len(connected) == 2:
                a, b = connected
                if node in edges[a] and node in edges[b]:
                    combined_dist = connected[a] + connected[b]
                    edges[a][b] = combined_dist
                    edges[b][a] = combined_dist
                    del edges[a][node]
                    del edges[b][node]
                    del edges[node]
                    break
        else:
            break

    START = (0, 1)
    END = (grid.shape[0]-1, grid.shape[1]-2)
    routes = [(START, 0, set())]
    longest = 0
    while routes:
        pt, dist, visited = routes.pop()
        if pt in visited:
            continue
        if pt == END:
            longest = max(longest, dist)
            continue
        visited.add(pt)
        for node, weight in edges[pt].items():
            routes.append((node, dist+weight, visited.copy()))
    return longest

def part2(grid):
    for pt, val in np.ndenumerate(grid):
        if val in '^v><':
            grid[pt] = '.'
    return part1(grid)

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    grid = np.array([list(l) for l in lines])
    return [grid]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 2210

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 6522

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (94, 154)
    TEST_INPUT = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
