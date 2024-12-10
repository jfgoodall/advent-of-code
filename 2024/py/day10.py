#!/usr/bin/env python3
import time
import typing
from functools import lru_cache
from io import StringIO

# make grid global so it doesn't have to be hashed every time
# get_reachable_peaks is called; order of magnitude faster than passing
# grid as parameter
GRID = tuple()

@lru_cache
def get_reachable_peaks(row, col, step_height):
    if (
        row < 0 or row >= len(GRID) or
        col < 0 or col >= len(GRID[0]) or
        GRID[row][col] != step_height
    ):
        return tuple()

    if GRID[row][col] == 9:
        return ((row, col),)

    return (
        get_reachable_peaks(row-1, col, GRID[row][col]+1) +
        get_reachable_peaks(row+1, col, GRID[row][col]+1) +
        get_reachable_peaks(row, col-1, GRID[row][col]+1) +
        get_reachable_peaks(row, col+1, GRID[row][col]+1)
    )

def part1():
    score = 0
    for r, row in enumerate(GRID):
        for c, height in enumerate(row):
            if height == 0:
                peaks = get_reachable_peaks(r, c, 0)
                score += len(set(peaks))
    return score

def part2():
    score = 0
    for r, row in enumerate(GRID):
        for c, height in enumerate(row):
            if height == 0:
                peaks = get_reachable_peaks(r, c, 0)
                score += len(peaks)
    return score

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    global GRID

    data_src.seek(0)
    GRID = tuple(
        tuple(map(int, list(line))) for line in data_src.read().splitlines()
    )
    return []

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # -

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # -

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    TEST_ANSWER1 = 36

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 81

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
