#!/usr/bin/env python3
import itertools
import time
from io import StringIO
from pprint import pprint

DELTA = { 'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1) }

def part1_(plan):
    grid = set()
    pos = (0, 0)
    for direction, length, _ in plan:
        dxy = DELTA[direction]
        for _ in range(length):
            pos = (pos[0]+dxy[0], pos[1]+dxy[1])
            grid.add(pos)

    min_x = min(grid)[0]
    max_x = max(grid)[0]
    min_y = min(grid, key=lambda x: x[1])[1]
    max_y = max(grid, key=lambda x: x[1])[1]
    fill = []
    for x in range(min_x, max_x+1):
        if (x, min_y) not in grid:
            fill.append((x, min_y))
    for x in range(min_x, max_x+1):
        if (x, max_y) not in grid:
            fill.append((x, max_y))
    for y in range(min_y+1, max_y):
        if (min_x, y) not in grid:
            fill.append((min_x, y))
    for y in range(min_y+1, max_y):
        if (max_x, y) not in grid:
            fill.append((max_x, y))

    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1):
            if (x,y) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

    # flood fill the outside
    outside = set()
    progress = 0
    while fill:
        progress += 1
        if progress % 100000 == 0:
            print(len(fill))
        pos = fill.pop()
        if not (min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y):
            continue

        if pos not in grid:
            outside.add(pos)
            grid.add(pos)
            fill.append((pos[0]+1, pos[1]))
            fill.append((pos[0]-1, pos[1]))
            fill.append((pos[0], pos[1]+1))
            fill.append((pos[0], pos[1]-1))

    return (max_x-min_x+1) * (max_y-min_y+1) - len(outside)

def part1(plan):
    vert = set()
    horz = set()
    lines = set()

    start = (0, 0)
    for direction, length, _ in plan:
        dxy = DELTA[direction]
        end = (start[0]+(dxy[0]*length), start[1]+(dxy[1]*length))
        if direction in 'UD':
            vert.add(end[0])
        else:
            horz.add(end[1])
        lines.add((start, end))
        start = end

    pprint(sorted(vert))
    pprint(sorted(horz))
    pprint(lines)

    compact = []
    for y1, y2 in itertools.pairwise(reversed(sorted(horz))):
        row = []
        for x1, x2 in itertools.pairwise(sorted(vert)):
            row.append(((x1, y1), abs(x2-x1), abs(y2-y1)))
        compact.append(row)
    pprint(compact)

    total = 0
    for row in compact:
        for col in row:
            total += col[1] * col[2]
    print(total)

def translate_plan(plan):
    DIR_MAP = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    new_plan = []
    for _, _, color in plan:
        new_plan.append((DIR_MAP[color[-2]], int(color[2:-2], base=16), color))
    return new_plan

def part2(plan):
    plan = translate_plan(plan)

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
        assert part1(*parse_input(test_data)) == test_answers[0]
        # print_result('1', part1, *parse_input(infile))  # 48400

        # assert part2(*parse_input(test_data)) == test_answers[1]
        # print_result('2', part2, *parse_input(infile))  #

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
