#!/usr/bin/env python3
import time, itertools, functools, re, random
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
from dataclasses import dataclass
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

@dataclass
class Player:
    pos: int = 0
    score: int = 0
    turns: int = 0

class Node:
    __slots__ = 'pos', 'score', 'left', 'center', 'right'
    def __init__(self, pos):
        self.pos = pos
        self.score = 0
        self.left = None
        self.center = None
        self.right = None

def part1(p1_pos, p2_pos):
    p1, p2 = Player(pos=p1_pos), Player(pos=p2_pos)
    die = itertools.cycle(range(1, 101))

    while True:
        roll = sum(next(die) for _ in range(3))
        p1.pos = (p1.pos+roll-1)%10 + 1
        p1.score += p1.pos
        p1.turns += 1
        if p1.score >= 1000:
            break
        p1, p2 = p2, p1

    return p2.score * (p1.turns+p2.turns)*3

def part2(p1_pos, p2_pos):
    root = Node(p1_pos)
    leaves = 0
    def build_tree(node, depth=0):
        print(f'depth: {depth}, pos: {node.pos}, score: {node.score}')
        for val, child in enumerate((node.left, node.center, node.right), 1):
            child = Node((node.score+val-1)%10+1)
            child.score = node.score + child.pos
            if child.score < 21:
                build_tree(child, depth+1)
            else:
                nonlocal leaves
                leaves += 1
    build_tree(root)
    print("leaves:", leaves)

def parse_input(data_src):
    data_src.seek(0)
    p1 = int(next(data_src).split()[-1])
    p2 = int(next(data_src).split()[-1])
    return p1, p2

def run_tests():
    TEST_INPUT = """
Player 1 starting position: 4
Player 2 starting position: 8
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(*parse_input(test_data)) == 739785
    assert part2(*parse_input(test_data)) == 444356092776315

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, *parse_input(infile))  # -
    #     print_result('2', part2, *parse_input(infile))  # -
