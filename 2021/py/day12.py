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

def may_visit_p1(node, path):
    return node.isupper() or node not in path

def may_visit_p2(node, path):
    if node.isupper() or node not in path:
        return True
    small_caves = list(filter(str.islower, path))
    return len(small_caves) == len(set(small_caves))

def count_paths(edges, visit_rule, current_path=['start']):
    if current_path[-1] == 'end':
        return 1

    found_paths = 0
    for node in edges[current_path[-1]]:
        if node != 'start' and visit_rule(node, current_path):
            found_paths += count_paths(edges, visit_rule, current_path+[node])
    return found_paths

def part1(edges):
    return count_paths(edges, may_visit_p1)

def part2(edges):
    return count_paths(edges, may_visit_p2)

def parse_input(data_src):
    data_src.seek(0)
    edges = defaultdict(list)
    for line in data_src:
        a, b = line.strip().split('-')
        edges[a].append(b)
        edges[b].append(a)
    return edges

def run_tests():
    TEST_INPUT = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 10
    assert part2(parse_input(test_data)) == 36

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 4411
        print_result('2', part2, parse_input(infile))  # 136767
