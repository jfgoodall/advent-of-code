#!/usr/bin/env python3
import os
import sys
import time
from io import StringIO

sys.path.append(os.path.dirname(__file__))
from common_patterns.math import popcount

DIR_MAP = {
    '.': 0,
    '<': 1,
    '>': 2,
    '^': 4,
    'v': 8
}

def dump(valley, locations=set()):
    for row, line in enumerate(valley):
        for col, ch in enumerate(line):
            if isinstance(ch, str):
                print(ch, end='')
            else:
                if ch == 0:
                    if (row, col) in locations:
                        print('E', end='')
                    else:
                        print('.', end='')
                elif ch == 1:
                    print('<', end='')
                elif ch == 2:
                    print('>', end='')
                elif ch == 4:
                    print('^', end='')
                elif ch == 8:
                    print('v', end='')
                else:
                    print(popcount(ch), end='')
        print()

def advance_blizzards(valley):
    height = len(valley) - 2
    width = len(valley[0]) - 2
    new = []
    new.append(list(valley[0]))
    for _ in range(height):
        new.append(['#'] + [0 for _ in range(width)] + ['#'])
    new.append(list(valley[-1]))

    for row in range(1, height+1):
        for col in range(1, width+1):
            if valley[row][col] & 1:
                new[row][(col-2)%width+1] |= 1
            if valley[row][col] & 2:
                new[row][col%width+1] |= 2
            if valley[row][col] & 4:
                new[(row-2)%height+1][col] |= 4
            if valley[row][col] & 8:
                new[row%height+1][col] |= 8
    return new

def walk(t, valley, start, goal):
    locations = set()
    locations.add(start)
    while True:
        if goal in locations:
            return t, valley

        t += 1
        valley = advance_blizzards(valley)
        next_loc = set()
        for row, col in locations:
            # check up
            if row-1 >= 0 and valley[row-1][col] == 0:
                next_loc.add((row-1, col))
            # check down
            if row+1 < len(valley) and valley[row+1][col] == 0:
                next_loc.add((row+1, col))
            # check left
            if valley[row][col-1] == 0:
                next_loc.add((row, col-1))
            # check right
            if valley[row][col+1] == 0:
                next_loc.add((row, col+1))
            # check wait
            if valley[row][col] == 0:
                next_loc.add((row, col))
        locations = next_loc

def part1(valley):
    start = (0, 1)
    goal = (len(valley)-1, len(valley[0])-2)

    t, _ = walk(0, valley, start, goal)
    return t

def part2(valley):
    start = (0, 1)
    goal = (len(valley)-1, len(valley[0])-2)

    t, valley = walk(0, valley, start, goal)
    t, valley = walk(t, valley, goal, start)
    t, valley = walk(t, valley, start, goal)
    return t

def parse_input(data_src):
    data_src.seek(0)
    valley = []
    for line in data_src.read().splitlines():
        line = list(line)
        for idx, ch in enumerate(line):
            if ch in DIR_MAP:
                line[idx] = DIR_MAP[ch]
        valley.append(line)
    return [valley]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 314

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 896

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (18, 54)
    TEST_INPUT = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
