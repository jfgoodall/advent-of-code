#!/usr/bin/env python3
import itertools
import time
import typing
from io import StringIO

import shapely


def part1(coords):
    hull = list(shapely.MultiPoint(coords).convex_hull.exterior.coords)
    rects = itertools.combinations(hull[:-1], 2)
    areas = [(abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1) for a, b in rects]
    return max(areas)

def part2(coords):
    poly = shapely.Polygon(coords)
    max_area = 0
    for a, b in itertools.combinations(coords, 2):
        if poly.covers(shapely.Polygon([a, (a[0], b[1]), b, (b[0], a[1])])):
            area = (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)
            if area > max_area:
                max_area = area
    return max_area

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [list(tuple(map(int, line.split(','))) for line in data_src.read().splitlines())]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=4767418746)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=1461987144)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
    TEST_ANSWER1 = 50

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 24

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
