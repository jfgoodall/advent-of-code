#!/usr/bin/env python3
import time
import typing
from io import StringIO


def part1(lines):
    ROWS = len(lines)
    COLS = len(lines[0])
    VECTORS = [
        (0, 1), (0, -1),   # horizontal
        (1, 0), (-1, 0),   # vertical
        (1, 1), (-1, -1),  # diagonal 1
        (1, -1), (-1, 1)   # diagonal 2
    ]

    total = 0
    for row in range(ROWS):
        for col in range(COLS):
            for vec in VECTORS:
                r, c = row, col
                for ch in 'XMAS':
                    if (
                        r < 0 or r >= ROWS or
                        c < 0 or c >= COLS or
                        lines[r][c] != ch
                    ):
                        break
                    r += vec[0]
                    c += vec[1]
                else:
                    total += 1
    return total

def part2(lines):
    ROWS = len(lines)
    COLS = len(lines[0])

    def valid_coord(row, col):
        return 0 <= row < ROWS and 0 <= col < COLS

    total = 0
    for row in range(1, ROWS-1):
        for col in range(1, COLS-1):
            if (
                (
                    lines[row][col] == 'A' and
                    valid_coord(row-1, col-1) and
                    valid_coord(row-1, col+1) and
                    valid_coord(row+1, col-1) and
                    valid_coord(row+1, col+1)
                ) and (
                    lines[row-1][col-1] == 'M' and lines[row+1][col+1] == 'S' or
                    lines[row-1][col-1] == 'S' and lines[row+1][col+1] == 'M'
                ) and (
                    lines[row-1][col+1] == 'M' and lines[row+1][col-1] == 'S' or
                    lines[row-1][col+1] == 'S' and lines[row+1][col-1] == 'M'
                )
            ):
                total += 1
    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read().splitlines()]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test1_data)) == test1_answer
        solve_part('1', part1, *parse_input(infile))  # 2536

        assert part2(*parse_input(test2_data)) == test2_answer
        solve_part('2', part2, *parse_input(infile))  # 1875

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[(str, str|float) * 2]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    TEST_ANSWER1 = 18

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 9

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
