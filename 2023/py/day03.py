#!/usr/bin/env python3
from __future__ import annotations

import itertools
import re
import time
from dataclasses import dataclass
from io import StringIO

NUM_RE = re.compile(r'\d+')
STAR_RE = re.compile(r'\*')


@dataclass(frozen=True)
class PartNumber:
    val: int
    row: int
    span: tuple(int, int)


def find_part_numbers(grid_lines):
    for row, line in enumerate(grid_lines):
        for match in NUM_RE.finditer(line):
            yield PartNumber(int(match.group()), row, match.span())

def find_stars(grid_lines):
    for row, line in enumerate(grid_lines):
        for match in STAR_RE.finditer(line):
            yield (row, match.span()[0])

def part1(lines):
    LEN = len(lines[0])

    total = 0
    for num in find_part_numbers(lines):
        row_span = (max(0, num.row-1), min(len(lines), num.row+1+1))
        col_span = (max(0, num.span[0]-1), min(LEN, num.span[1]+1))
        for row, col in itertools.product(range(*row_span), range(*col_span)):
            if lines[row][col] not in '.0123456789':
                total += num.val
                break
    return total

def part2(lines):
    LEN = len(lines[0])

    total = 0
    nums = list(find_part_numbers(lines))
    for row, col in find_stars(lines):
        adj_pts = {
            (max(0, row-1),   max(0, col-1)),
            (max(0, row-1),   col),
            (max(0, row-1),   min(LEN, col+1)),
            (row,             max(0, col-1)),
            (row,             min(LEN, col+1)),
            (min(LEN, row+1), max(0, col-1)),
            (min(LEN, row+1), col),
            (min(LEN, row+1), min(LEN, col+1)),
        }

        candidates = set()
        for pt in adj_pts:
            for num in nums:
                if pt[0] == num.row and pt[1] >= num.span[0] and pt[1] < num.span[1]:
                    candidates.add(num)
                    break

        if len(candidates) == 2:
            total += candidates.pop().val * candidates.pop().val

    return total

def parse_input(data_src):
    data_src.seek(0)
    return [data_src.read().splitlines()]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 525181

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 84289137

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (4361, 467835)
    TEST_INPUT = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
