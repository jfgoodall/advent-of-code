#!/usr/bin/env python3
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

@dataclass
class Node:
    idx: int
    val: int
    next: Node=None
    prev: Node=None

def dump(node):
    start = node
    while node.next is not start:
        print(node.val, end=' ')
        node = node.next
    print(node.val)

def part1(parsed):
    head = Node(0, parsed[0])
    curr = head
    for idx, val in enumerate(parsed[1:], 1):
        curr.next = Node(idx, val, prev=curr)
        curr = curr.next
        if val == 0:
            zero = curr
    curr.next = head
    head.prev = curr

    for idx in tqdm(range(len(parsed))):
        while curr.idx != idx:
            curr = curr.next

        if not curr.val:
            continue

        # remove curr from linked list
        bookmark = curr.prev
        curr.prev.next = curr.next
        curr.next.prev = curr.prev

        if curr.val > 0:
            for _ in range(curr.val):
                bookmark = bookmark.next
        else:
            for _ in range(abs(curr.val)):
                bookmark = bookmark.prev

        # insert curr after bookmark
        curr.next = bookmark.next
        curr.prev = bookmark
        curr.prev.next = curr
        curr.next.prev = curr

    total = 0
    for _ in range(3):
        for _ in range(1000):
            zero = zero.next
        total += zero.val
    return total

def part2(parsed):
    KEY = 811589153

    head = Node(0, parsed[0]*KEY)
    curr = head
    for idx, val in enumerate(parsed[1:], 1):
        curr.next = Node(idx, val*KEY, prev=curr)
        curr = curr.next
        if val == 0:
            zero = curr
    curr.next = head
    head.prev = curr

    for idx in tqdm(list(itertools.chain(*itertools.repeat(range(len(parsed)), 10)))):
        while curr.idx != idx:
            curr = curr.next

        if not curr.val:
            continue

        # remove curr from linked list
        bookmark = curr.prev
        curr.prev.next = curr.next
        curr.next.prev = curr.prev

        for _ in range(abs(curr.val) % (len(parsed)-1)):
            if curr.val > 0:
                bookmark = bookmark.next
            else:
                bookmark = bookmark.prev

        # insert curr after bookmark
        curr.next = bookmark.next
        curr.prev = bookmark
        curr.prev.next = curr
        curr.next.prev = curr

    total = 0
    for _ in range(3):
        for _ in range(1000):
            zero = zero.next
        total += zero.val
    return total

def parse_input(data_src):
    data_src.seek(0)
    parsed = list(map(int, data_src.read().splitlines()))
    return [parsed]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 5498

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 3390007892081

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (3, 1623178306)
    TEST_INPUT = """
1
2
-3
3
-2
0
4
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
