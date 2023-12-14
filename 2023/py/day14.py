#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np


def calc_load(platform):
    return sum(platform.shape[0]-row
               for (row, _), val in np.ndenumerate(platform) if val == 'O')

def tilt_north(platform):
    for col in range(platform.shape[0]):
        while True:
            for row in range(1, platform.shape[1]):
                if platform[row,col] == 'O' and platform[row-1,col] == '.':
                    platform[row,col] = '.'
                    platform[row-1,col] = 'O'
                    break
            else:
                break

def tilt_west(platform):
    for row in range(platform.shape[1]):
        while True:
            for col in range(1, platform.shape[0]):
                if platform[row,col] == 'O' and platform[row,col-1] == '.':
                    platform[row,col] = '.'
                    platform[row,col-1] = 'O'
                    break
            else:
                break

def tilt_south(platform):
    for col in range(platform.shape[0]):
        while True:
            for row in range(1, platform.shape[1]):
                if platform[row,col] == '.' and platform[row-1,col] == 'O':
                    platform[row,col] = 'O'
                    platform[row-1,col] = '.'
                    break
            else:
                break

def tilt_east(platform):
    for row in range(platform.shape[1]):
        while True:
            for col in range(1, platform.shape[0]):
                if platform[row,col] == '.' and platform[row,col-1] == 'O':
                    platform[row,col] = 'O'
                    platform[row,col-1] = '.'
                    break
            else:
                break

def part1(platform):
    tilt_north(platform)
    return calc_load(platform)

def part2(platform):
    seen = {}
    plats = []
    for cycle in range(1, 1_000_000_000):
        tilt_north(platform)
        tilt_west(platform)
        tilt_south(platform)
        tilt_east(platform)

        plat = tuple(map(tuple, platform))
        if plat in seen:
            offset = seen[plat] - 1
            period = cycle - seen[plat]
            break
        seen[plat] = cycle
        plats.append(plat)

    p = (1_000_000_000-offset) % period + offset
    return calc_load(np.array(plats[p-1]))

def parse_input(data_src):
    data_src.seek(0)
    lines = data_src.read().splitlines()
    platform = np.array([list(l) for l in lines])
    return [platform]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 109654

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 94876

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (136, 64)
    TEST_INPUT = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
