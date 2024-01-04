#!/usr/bin/env python3
import multiprocessing
import time
from io import StringIO

import numpy as np


def calc_load(platform):
    return sum(platform.shape[0]-row
               for (row, _), val in np.ndenumerate(platform) if val == 'O')

def tilt_lane(lane, direction):
    dest_bound = lane.shape[0] if direction == -1 else -1
    dest = 0 if direction == -1 else lane.shape[0]-1

    while dest != dest_bound and lane[dest] != '.':
        dest -= direction
    src = dest - direction

    while 0 <= src < lane.shape[0]:
        if lane[src] in 'O#':
            if lane[src] == 'O':
                lane[src] = '.'
                lane[dest] = 'O'
            else:
                dest = src
            dest -= direction

            while dest != dest_bound and lane[dest] != '.':
                dest -= direction
            src = dest
        src -= direction
    return lane

def tilt_north(platform):
    tilted = pool.starmap(tilt_lane, ((col, -1) for col in platform.T))
    return np.array(tilted).T

def tilt_west(platform):
    tilted = pool.starmap(tilt_lane, ((row, -1) for row in platform))
    return np.array(tilted)

def tilt_south(platform):
    tilted = pool.starmap(tilt_lane, ((col, +1) for col in platform.T))
    return np.array(tilted).T

def tilt_east(platform):
    tilted = pool.starmap(tilt_lane, ((row, +1) for row in platform))
    return np.array(tilted)

def part1(platform):
    platform = tilt_north(platform)
    return calc_load(platform)

def part2(platform):
    seen = {}
    plats = [platform]
    for cycle in range(1, 1_000_000_000):
        platform = tilt_north(platform)
        platform = tilt_west(platform)
        platform = tilt_south(platform)
        platform = tilt_east(platform)

        plat_hash = platform.tobytes()
        if plat_hash in seen:
            offset = seen[plat_hash] - 1
            period = cycle - seen[plat_hash]
            break
        seen[plat_hash] = cycle
        plats.append(platform)

    equivalent = plats[(1_000_000_000-offset) % period + offset]
    return calc_load(equivalent)

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

pool = multiprocessing.Pool()
if __name__ == '__main__':
    main()
