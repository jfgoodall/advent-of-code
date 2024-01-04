#!/usr/bin/env python3
from __future__ import annotations

import functools
import itertools
import os
import re
import sys
import time
from collections import Counter, defaultdict, namedtuple
from dataclasses import dataclass
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

# sys.path.append(os.path.dirname(__file__))
# from common_patterns.point import Point2D
# from common_patterns.itertools import pairwise

BLOCKS = [
    [list('..@@@@.')],

    [list('...@...'),
     list('..@@@..'),
     list('...@...')],

    # [list('....@..'),
    #  list('....@..'),
    #  list('..@@@..')],

    [list('..@@@..'),  # flip top-to-bottom to account for direction of growth
     list('....@..'),
     list('....@..')],

    [list('..@....'),
     list('..@....'),
     list('..@....'),
     list('..@....')],

    [list('..@@...'),
     list('..@@...')]
]

GAP = [
    list('.......'),
    list('.......'),
    list('.......')
]

def dump(cave):
    for row in reversed(cave):
        print(''.join(row))

def shift_left(cave, row_start, row_end):
    # check clearance
    for row in cave[row_start:row_end]:
        try:
            idx = row.index('@')
            if idx == 0 or row[idx-1] != '.':
                return
        except ValueError:
            pass

    # there is clearance to shift the block
    for row in cave[row_start:row_end]:
        for idx in range(len(row)-1):
            if row[idx+1] == '@':
                row[idx] = '@'
                row[idx+1] = '.'

def shift_right(cave, row_start, row_end):
    # check clearance
    for row in cave[row_start:row_end]:
        try:
            idx = len(row) - 1 - row[::-1].index('@')
            if idx == len(row)-1 or row[idx+1] != '.':
                return
        except ValueError:
            pass

    # there is clearance to shift the block
    for row in cave[row_start:row_end]:
        for i in range(len(row)-1, 0, -1):
            if row[i-1] == '@':
                row[i] = '@'
                row[i-1] = '.'

def shift_down(cave, row_start, row_end):
    # check clearance
    for col in range(len(cave[0])):
        for row in range(row_start, row_end):
            if cave[row][col] == '@':
                if row == 0 or cave[row-1][col] != '.':
                    return False
                break

    # there is clearance to shift the block
    for col in range(len(cave[0])):
        for row in range(row_start, row_end):
            if cave[row][col] == '@':
                cave[row-1][col] = '@'
                cave[row][col] = '.'
    return True

def drop_blocks(cave, num_blocks, direction_iter, block_iter):
    # cave[0] is on the bottom
    cave.extend(list(row) for row in GAP)
    cave.extend(list(row) for row in next(block_iter))

    dist = 0  # how far the current block has fallen
    while True:
        # limit which rows to mess with (block is in here)
        row_end = len(cave) - dist
        row_start = max(0, row_end-4)

        # push block left/right
        direction = next(direction_iter)
        if direction == '<':
            shift_left(cave, row_start, row_end)
        else:  # '>'
            shift_right(cave, row_start, row_end)

        # drop block
        if shift_down(cave, row_start, row_end):
            dist += 1
        else:
            # turn moving block into fixed (@ -> #)
            for row in cave[row_start:row_end]:
                for idx, x in enumerate(row):
                    if x == '@':
                        row[idx] = '#'

            # trim unpopulated top rows
            while all(x == '.' for x in cave[-1]):
                cave.pop()

            num_blocks -= 1
            if num_blocks == 0:
                break

            # add 3 space gap and next block
            cave.extend(list(row) for row in GAP)
            cave.extend(list(row) for row in next(block_iter))
            dist = 0
    return cave

def part1(directions):
    direction_iter = iter(itertools.cycle(directions))
    block_iter = iter(itertools.cycle(BLOCKS))
    cave = drop_blocks([], 2022, direction_iter, block_iter)
    return len(cave)

def encode_rocks(cave_rows):
    # convert cave rows to ints, using rocks as bits
    encoded = []
    table = str.maketrans({'.': '0', '#': '1'})
    for row in cave_rows:
        bits = ''.join(row).translate(table)
        encoded.append(int(bits, 2))
    return encoded

def find_period(cave, max_period):
    # linear search for a repeating pattern of length max_period
    encoded = encode_rocks(cave)

    # need to back up from end to find the last stable point as a reference
    # TODO
    substr = encoded[-max_period:]
    idx = len(encoded)
    while idx > max_period:
        idx -= 1
        if encoded[idx-max_period:idx] == substr:
            period = len(encoded) - idx  # actual period
            print('!!! found !!!')
            break
    assert idx > max_period
    assert encoded[-period:] == encoded[-period*2:-period]
    assert cave[-period:] == cave[-period*2:-period]
    return period

def part2(directions):
    direction_iter = iter(itertools.cycle(directions))
    block_iter = iter(itertools.cycle(BLOCKS))

    # run for 3x the max possible period length to generate at least 2 cycles
    max_period = len(BLOCKS) * len(directions)
    print('initial drop...', end='', flush=True)
    cave = drop_blocks([], max_period*4, direction_iter, block_iter)
    print('done')

    # find the period of the repeating pattern of the rocks
    print('calculating period...', end='', flush=True)
    period = find_period(cave, max_period)
    print(period)

    # determine how many blocks and how much height in a repeating cycle
    print('calculating blocks per cycle...', end='', flush=True)
    pattern = encode_rocks(cave[-period:])
    height_before = len(cave)
    for blocks_per_cycle in itertools.count(1):
        cave = drop_blocks(cave, 1, direction_iter, block_iter)
        if pattern == encode_rocks(cave[-period:]):
            break
    height_per_cycle = len(cave) - height_before
    print(blocks_per_cycle)

    blocks_to_drop = 1000000000000 - max_period*4 - blocks_per_cycle
    cycles_skipped = blocks_to_drop // blocks_per_cycle
    blocks_to_drop -= cycles_skipped * blocks_per_cycle

    # drop the remaining modulus blocks
    print('dropping remaining ', blocks_to_drop, 'rocks...', end='', flush=True)
    cave = drop_blocks(cave, blocks_to_drop, direction_iter, block_iter)
    print('done')

    return len(cave) + cycles_skipped * height_per_cycle

def parse_input(data_src):
    data_src.seek(0)
    return [data_src.read().strip()]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 3159

        assert part2(*parse_input(test_data)) == test_answers[1]
        print('!!! TEST PASSED !!!')
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (3068, 1514285714288)
    TEST_INPUT = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
