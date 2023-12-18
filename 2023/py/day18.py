#!/usr/bin/env python3
import functools
import time
from io import StringIO

import numpy as np


def calculate_area_rectangles(plan):
    """add rectangular areas when moving right, subtract them when moving left;
       this only works because polygon is defined rectilinearlly; use shoelace
       method (below) for general simple polygons"""
    area = 0
    perimeter = 0
    x, y = 0, 0
    for direction, length, _ in plan:
        perimeter += length
        match direction:
            case 'R':
                x += length
                area += length * y
            case 'L':
                x -= length
                area -= length * y
            case 'U':
                y += length
            case 'D':
                y -= length

    # account for the boundary line having width > 0
    return abs(area) + perimeter//2 + 1

def calculate_area_shoelace(plan):
    """use shoelace method to calculate polygon area:
       https://en.wikipedia.org/wiki/Shoelace_formula"""
    DIRECTION_MAP = {'R': np.array((1,0)), 'L': np.array((-1,0)),
                     'U': np.array((0,1)), 'D': np.array((0,-1))}
    areax2 = 0
    perimeter = 0
    a = np.array((0, 0))
    for direction, length, _ in plan:
        perimeter += length
        b = a + DIRECTION_MAP[direction]*length
        areax2 += a[0]*b[1] - b[0]*a[1]
        a = b

    # account for the boundary line having width > 0
    return abs(areax2//2) + perimeter//2 + 1

def part1(method, plan):
    return method(plan)

def part2(method, plan):
    DIR_MAP = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    new_plan = [(DIR_MAP[color[-2]], int(color[2:-2], base=16), color)
                for *_, color in plan]
    return method(new_plan)

def parse_input(data_src):
    data_src.seek(0)
    plan = []
    for line in data_src.read().splitlines():
        direction, length, color = line.split()
        plan.append((direction, int(length), color))
    return [plan]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        p1_rect = functools.partial(part1, calculate_area_rectangles)
        p1_shoe = functools.partial(part1, calculate_area_shoelace)
        assert p1_rect(*parse_input(test_data)) == test_answers[0]
        assert p1_shoe(*parse_input(test_data)) == test_answers[0]
        print_result('1 Rectangles', p1_rect, *parse_input(infile))  # 48400
        print_result('1 Shoelace  ', p1_shoe, *parse_input(infile))  # 48400

        p2_rect = functools.partial(part2, calculate_area_rectangles)
        p2_shoe = functools.partial(part2, calculate_area_shoelace)
        assert p2_rect(*parse_input(test_data)) == test_answers[1]
        assert p2_shoe(*parse_input(test_data)) == test_answers[1]
        print_result('2 Rectangles', p2_rect, *parse_input(infile))  # 72811019847283
        print_result('2 Shoelace  ', p2_shoe, *parse_input(infile))  # 72811019847283

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (62, 952408144115)
    TEST_INPUT = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
