#!/usr/bin/env python3
from __future__ import annotations

import functools
import itertools
import os
import re
import sys
import time
from collections import Counter, defaultdict, namedtuple
from dataclasses import dataclass
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

# sys.path.append(os.path.dirname(__file__))
# from common_patterns.point import Point2D
# from common_patterns.itertools import pairwise

Valve = namedtuple('Valve', 'label, flow_rate, neighbors')

def shortest_path(valves, start, end):
    def bfs(start, end, dist, used):
        if start == end:
            return dist
        used = set(used)
        used.add(start)
        paths = []
        for n in start.neighbors:
            neighbor = valves[n]
            if neighbor == end or (neighbor not in used and
                                   neighbor.flow_rate == 0):
                path_dist = bfs(neighbor, end, dist+1, used)
                if path_dist:
                    paths.append(path_dist)
        return min(paths) if paths else 0
    return bfs(start, end, 0, {})

def compress_graph(valves):
    useful = set(v for v in valves.values() if v.flow_rate)
    graph = defaultdict(list)
    for start in (valves['AA'], *useful):
        # find shortest path through 0's from target to other useful valves
        for end in useful:
            dist = shortest_path(valves, start, end)
            if dist:
                graph[start].append((end, dist))
    return graph

def part1(valves):
    graph = compress_graph(valves)

    # traveling salesman :(
    running_max = 0
    def find_max(valve, open_valves, time, pressure):
        nonlocal running_max
        if time <= 0 or len(open_valves) == 0:
            running_max = max(running_max, pressure)
            return pressure

        # ditch early if it's impossible to theoretically beat running_max
        theory_max = pressure
        theory_t = time
        for v in sorted(open_valves, key=lambda v: v.flow_rate, reverse=True):
            theory_max += v.flow_rate * theory_t
            theory_t -= 1
        if running_max > theory_max:
            return 0

        # try moving to all neighbors
        paths = [find_max(n, set(open_valves), time-dist, pressure)
                 for n, dist in graph[valve]]

        # try opening this valve
        if valve in open_valves:
            open_valves.remove(valve)
            pressure += valve.flow_rate * (time-1)
            paths.append(find_max(valve, open_valves, time-1, pressure))
        return max(paths)

    open_valves = set(graph)
    return find_max(valves['AA'], open_valves, 30, 0)

def part2(valves):
    graph = compress_graph(valves)

    # traveling salesman :(
    running_max = 0
    def find_max(p1, p2, t1, t2, open_valves, pressure):
        nonlocal running_max
        if (t1 <= 0 and t2 <= 0) or len(open_valves) == 0:
            running_max = max(running_max, pressure)
            return pressure

        # ditch early if it's impossible to theoretically beat running_max
        theory_max = pressure
        theory_t = max(t1, t2)
        for v in sorted(open_valves, key=lambda v: v.flow_rate, reverse=True):
            theory_max += v.flow_rate * theory_t
            theory_t -= 1
        if running_max > theory_max:
            return 0

        # try moving to all neighbors
        p1_paths = graph[p1]
        p2_paths = graph[p2]
        paths = [find_max(pp1[0], pp2[0], t1-pp1[1], t2-pp2[1],
                          set(open_valves), pressure)
                 for pp1, pp2 in itertools.product(p1_paths, p2_paths)]

        # try opening p1 valve
        if p1 in open_valves and t1 > 0:
            open_valves.remove(p1)
            pressure += p1.flow_rate * (t1-1)
            paths.append(find_max(p1, p2, t1-1, t2, open_valves, pressure))

        # try opening p1 valve
        if p2 in open_valves and t2 > 0:
            open_valves.remove(p2)
            pressure += p2.flow_rate * (t2-1)
            paths.append(find_max(p1, p2, t1, t2-1, open_valves, pressure))

        return max(paths)

    open_valves = set(graph)
    return find_max(valves['AA'], valves['AA'], 26, 26, open_valves, 0)

def parse_input(data_src):
    PARSE_RE = re.compile(r'Valve (\w\w).*rate=(\d+);.*valves? (.*)$')
    data_src.seek(0)
    valves = defaultdict(Valve)
    for line in data_src.read().splitlines():
        label, rate, neighbors = PARSE_RE.match(line).groups()
        valves[label] = Valve(label, int(rate),
                              tuple(n for n in neighbors.split(', ')))
    return [valves]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        # assert part1(*parse_input(test_data)) == test_answers[0]
        # print_result('1', part1, *parse_input(infile))  # -

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (1651, 1707)
    TEST_INPUT = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
