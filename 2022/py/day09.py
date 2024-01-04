#!/usr/bin/env python3
import os
import sys
import time
from io import StringIO

sys.path.append(os.path.dirname(__file__))
from common_patterns import Point2D, pairwise

HEAD_OFFSET = { 'R': Point2D((1, 0)),
                'L': Point2D((-1, 0)),
                'U': Point2D((0, 1)),
                'D': Point2D((0, -1)) }

def tail_offset(head, tail):
    def sign(x):
        if x > 0: return 1
        if x < 0: return -1
        return 0

    if abs(head.x-tail.x) > 1 or abs(head.y-tail.y) > 1:
        return Point2D((sign(head.x-tail.x), sign(head.y-tail.y)))
    return Point2D()

def part1(instr):
    head = Point2D()
    tail = Point2D()
    visited = {tuple(tail)}

    for direction, count in instr:
        for _ in range(count):
            head += HEAD_OFFSET[direction]
            tail += tail_offset(head, tail)
            visited.add(tuple(tail))
    return len(visited)

def part2(instr):
    knots = [Point2D() for _ in range(10)]
    visited = {tuple(knots[-1])}

    for direction, count in instr:
        for _ in range(count):
            knots[0] += HEAD_OFFSET[direction]
            for head, tail in pairwise(knots):
                tail += tail_offset(head, tail)
            visited.add(tuple(knots[-1]))
    return len(visited)

def parse_input(data_src):
    data_src.seek(0)
    return map(lambda x: (x[0], int(x[1])),
               (line.split() for line in data_src.read().splitlines()))

def main():
    test_data, test_answers = get_test_data()

    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(parse_input(test_data)) == test_answers[0]
        print_result('1', part1, parse_input(infile))  # 6212

        assert part2(parse_input(test_data)) == test_answers[1]
        print_result('2', part2, parse_input(infile))  # 2522

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test input and answers out of the way at the bottom of the file."""
    TEST_INPUT = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    TEST_RESULTS = (13, 1)

    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
