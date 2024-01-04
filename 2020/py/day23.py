#!/usr/bin/env python3
from collections import deque

def rotate_cups(cups):
    sz = len(cups)

    cups.rotate(-1)
    cargo = tuple(cups.popleft() for _ in range(3))

    dest = (cups[-1] - 2 + sz) % sz + 1
    while dest in cargo:
        dest = (dest - 2 + sz) % sz + 1

    idx = cups.index(dest)
    for cup in reversed(cargo):
        cups.insert(idx+1, cup)

def part1(cups, moves=100):
    for _ in range(moves):
        rotate_cups(cups)

    idx = cups.index(1)
    cups.rotate(-idx)
    return ''.join(map(str, list(cups)[1:]))

class Node:
    def __init__(self, cup, nxt=None):
        self.cup = cup
        self.nxt = nxt

    def __repr__(self):
        return f'Cup<{self.cup}>'

    def __str__(self):
        return str(self.cup)

def make_ring(cups, total_nodes=None):
    lst = list(cups)
    ring = Node(lst[0])
    lookup = {lst[0]: ring}
    head = ring
    for cup in lst[1:]:
        n = Node(cup)
        lookup[cup] = n
        ring.nxt = n
        ring = n

    if total_nodes is not None:
        for cup in range(len(cups)+1, total_nodes+1):
            n = Node(cup)
            lookup[cup] = n
            ring.nxt = n
            ring = n
    ring.nxt = head

    return head, lookup

def part1_b(cups, moves=100):
    sz = len(cups)
    current, lookup = make_ring(cups)
    for _ in range(moves):
        excision = current.nxt
        current.nxt = current.nxt.nxt.nxt.nxt

        dest = (current.cup - 2) % sz + 1
        while dest in (excision.cup, excision.nxt.cup, excision.nxt.nxt.cup):
            dest = (dest - 2) % sz + 1

        insertion = lookup[dest]
        excision.nxt.nxt.nxt = insertion.nxt
        insertion.nxt = excision

        current = current.nxt

    output = [None] * (sz-1)
    current = lookup[1].nxt
    for i in range(sz-1):
        output[i] = str(current.cup)
        current = current.nxt
    return ''.join(output)

def part2(cups):
    cups = deque(list(cups) + list(range(10, 1000001)), maxlen=1000000)
    assert len(cups) == 1000000
    move = 0
    for _ in range(10000000):
        rotate_cups(cups)
        move += 1
        if move & 0xff == 0:
            print(move)
    idx = cups.index(1)
    cups.rotate(-idx)
    return cups[1] * cups[2]

def part2_b(cups):
    sz = 1000000
    current, lookup = make_ring(cups, sz)
    for _ in range(10000000):
        excision = current.nxt
        current.nxt = current.nxt.nxt.nxt.nxt

        dest = (current.cup - 2) % sz + 1
        while dest in (excision.cup, excision.nxt.cup, excision.nxt.nxt.cup):
            dest = (dest - 2) % sz + 1

        insertion = lookup[dest]
        excision.nxt.nxt.nxt = insertion.nxt
        insertion.nxt = excision

        current = current.nxt

    current = lookup[1]
    return current.nxt.cup * current.nxt.nxt.cup

def parse_input(data):
    return deque(map(int, list(data)), maxlen=len(data))

def run_tests():
    test_input = "389125467"
    cups = parse_input(test_input)
    assert part1(cups, 10) == '92658374'
    assert part1_b(parse_input(test_input), 10) == '92658374'
    # assert part2(parse_input(test_input)) == 149245887792
    # assert part2_b(parse_input(test_input)) == 149245887792

if __name__ == '__main__':
    run_tests()
    print(f"Part 1: {part1_b(parse_input('583976241'))}")
    print(f"Part 2: {part2_b(parse_input('583976241'))}")
