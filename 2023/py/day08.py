#!/usr/bin/env python3
import itertools
import re
import time
from io import StringIO

import numpy as np


def part1(instr, network):
    node = 'AAA'
    for steps, direction in enumerate(itertools.cycle(instr), start=1):
        node = network[node][direction]
        if node == 'ZZZ':
            return steps

def part2(instr, network):
    # it took some manually playing with the data to see that each starting node
    # cycled around to an ending node with a specific frequency
    periods = []
    starting_nodes = [n for n in network if n[-1] == 'A']
    for node in starting_nodes:
        for steps, direction in enumerate(itertools.cycle(instr), start=1):
            node = network[node][direction]
            if node[-1] == 'Z':
                periods.append(steps)
                break
    return np.lcm.reduce(periods)

def parse_input(data_src):
    NODE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")

    data_src.seek(0)
    instr = [0 if c == 'L' else 1 for c in data_src.readline().strip()]
    data_src.readline()
    network = {}
    for line in data_src.read().splitlines():
        src, l_dest, r_dest = NODE_RE.match(line).groups()
        network[src] = (l_dest, r_dest)
    return [instr, network]

def main():
    with open(__file__[:-3] + '-input.dat') as infile:
        test_data, test_answers = get_test_data_1()
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 16697

        test_data, test_answers = get_test_data_2()
        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 10668805667831

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data_1():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (2, 0)
    TEST_INPUT = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

def get_test_data_2():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (2, 6)
    TEST_INPUT = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
