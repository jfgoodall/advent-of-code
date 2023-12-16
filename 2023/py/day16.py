#!/usr/bin/env python3
import time
from collections import deque
from io import StringIO

import numpy as np


def energized_tiles(layout, start_row, start_col, start_direction):
    HEIGHT = len(layout)
    WIDTH = len(layout[0])

    visited = set()
    tiles = deque([(start_row, start_col, start_direction)])

    while tiles:
        tile = tiles.pop()
        if (tile[0] < 0 or tile[0] >= HEIGHT or
            tile[1] < 0 or tile[1] >= WIDTH or
            tile in visited):
            continue

        visited.add(tile)

        match layout[tile[0],tile[1]], tile[2]:
            case ('.', 'right') | ('/', 'up') | ('\\', 'down') | ('-', 'right'):
                tiles.append((tile[0], tile[1]+1, 'right'))

            case ('.', 'left') | ('/', 'down') | ('\\', 'up') | ('-', 'left'):
                tiles.append((tile[0], tile[1]-1, 'left'))

            case ('.', 'down') | ('/', 'left') | ('\\', 'right') | ('|', 'down'):
                tiles.append((tile[0]+1, tile[1], 'down'))

            case ('.', 'up') | ('/', 'right') | ('\\', 'left') | ('|', 'up'):
                tiles.append((tile[0]-1, tile[1], 'up'))

            case ('|', 'right') | ('|', 'left'):
                tiles.append((tile[0]+1, tile[1], 'down'))
                tiles.append((tile[0]-1, tile[1], 'up'))

            case ('-', 'down') | ('-', 'up'):
                tiles.append((tile[0], tile[1]+1, 'right'))
                tiles.append((tile[0], tile[1]-1, 'left'))

    return len({(r, c) for (r, c, _) in visited})

def part1(layout):
    return energized_tiles(layout, 0, 0, 'right')

def part2(layout):
    HEIGHT = len(layout)
    WIDTH = len(layout[0])

    counts = []
    for row in range(HEIGHT):
        counts.append(energized_tiles(layout, row, 0, 'right'))
        counts.append(energized_tiles(layout, row, WIDTH-1, 'left'))
    for col in range(WIDTH):
        counts.append(energized_tiles(layout, 0, col, 'down'))
        counts.append(energized_tiles(layout, HEIGHT-1, col, 'up'))
    return max(counts)

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    layout = np.array([list(l) for l in lines])
    return [layout]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 8146

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 8358

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (46, 51)
    TEST_INPUT = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
