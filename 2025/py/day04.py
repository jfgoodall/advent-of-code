#!/usr/bin/env python3
import time
import typing
from io import StringIO


def is_roll(grid, row, col):
    assert len(grid) > 0 and len(grid[0]) > 0
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    return grid[row][col] == '@'

def is_roll_accessible(grid, row, col):
    num_rolls = (
        int(is_roll(grid, row-1, col-1)) +
        int(is_roll(grid, row-1, col)) +
        int(is_roll(grid, row-1, col+1)) +
        int(is_roll(grid, row, col-1)) +
        int(is_roll(grid, row, col+1)) +
        int(is_roll(grid, row+1, col-1)) +
        int(is_roll(grid, row+1, col)) +
        int(is_roll(grid, row+1, col+1))
    )
    return num_rolls < 4

def part1(grid):
    accessible = 0
    for row, line in enumerate(grid):
        for col, elem in enumerate(line):
            if elem == '@':
                accessible += is_roll_accessible(grid, row, col)
    return accessible

def copy_grid(grid):
    return [line.copy() for line in grid]

def remove_accessible_rolls(grid):
    grid_orig = copy_grid(grid)
    removed = 0
    for row, line in enumerate(grid_orig):
        for col, elem in enumerate(line):
            if elem == '@' and is_roll_accessible(grid_orig, row, col):
                grid[row][col] = '.'
                removed += 1
    return removed

def part2(grid):
    total_removed = 0
    while removed := remove_accessible_rolls(grid):
        total_removed += removed
    return total_removed

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [[list(l) for l in data_src.read().splitlines()]]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=1370)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=8437)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()
    TEST_ANSWER1 = 13

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 43

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
