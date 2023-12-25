#!/usr/bin/env python3
import time
from collections import defaultdict
from io import StringIO

import networkx as nx


# https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
# started implementing this and noticed it's included in networkx
def part1(wires):
    graph = nx.Graph()
    for src, dests in wires.items():
        for dest in dests:
            graph.add_edge(src, dest, weight=1)

    cut_value, partition = nx.stoer_wagner(graph)
    return len(partition[0]) * len(partition[1])

def parse_input(data_src):
    data_src.seek(0)
    wires = defaultdict(set)
    for line in data_src.read().splitlines():
        src, dests = line.split(': ')
        for dest in dests.split():
            wires[src].add(dest)
            wires[dest].add(src)
    return [wires]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 562772

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (54, 0)
    TEST_INPUT = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
