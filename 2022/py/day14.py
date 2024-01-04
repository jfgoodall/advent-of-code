#!/usr/bin/env python3
import os
import sys
import time
from collections import namedtuple
from io import StringIO

sys.path.append(os.path.dirname(__file__))
from common_patterns.itertools import pairwise

Point = namedtuple('Point', 'x, y')

def part1(cave):
    num_rocks = len(cave)
    min_x = min(pt.x for pt in cave)
    max_x = max(pt.x for pt in cave)
    max_y = max(pt.y for pt in cave)

    ORIGIN = Point(500, 0)
    sand = ORIGIN
    while True:
        if sand.x < min_x or sand.x > max_x or sand.y == max_y:
            break

        if (sand.x, sand.y+1) not in cave:
            sand = Point(sand.x, sand.y+1)
        elif (sand.x-1, sand.y+1) not in cave:
            sand = Point(sand.x-1, sand.y+1)
        elif (sand.x+1, sand.y+1) not in cave:
            sand = Point(sand.x+1, sand.y+1)
        else:
            cave.add(sand)
            sand = ORIGIN

    return len(cave) - num_rocks

def part2(cave):
    num_rocks = len(cave)
    max_y = max(pt.y for pt in cave)

    ORIGIN = Point(500, 0)
    sand = ORIGIN
    while True:
        if (sand.x, sand.y+1) not in cave:
            sand = Point(sand.x, sand.y+1)
        elif (sand.x-1, sand.y+1) not in cave:
            sand = Point(sand.x-1, sand.y+1)
        elif (sand.x+1, sand.y+1) not in cave:
            sand = Point(sand.x+1, sand.y+1)
        else:
            cave.add(sand)
            if sand == ORIGIN:
                break
            sand = ORIGIN

        if sand.y == max_y + 1:
            cave.add(sand)
            sand = ORIGIN

    return len(cave) - num_rocks

def parse_input(data_src):
    data_src.seek(0)

    paths = []
    for line in data_src.read().splitlines():
        pts = [Point(*map(int, pt.split(','))) for pt in line.split(' -> ')]
        paths.append(pts)

    cave = set()
    for path in paths:
        for a, b in pairwise(path):
            for x in range(min(a.x, b.x), max(a.x, b.x)+1):
                for y in range(min(a.y, b.y), max(a.y, b.y)+1):
                    cave.add(Point(x, y))

    return [cave]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 698

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 28594

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (24, 93)
    TEST_INPUT = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
