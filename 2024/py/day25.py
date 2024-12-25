#!/usr/bin/env python3
import itertools
import time
import typing
from io import StringIO


def part1(locks, keys):
    return sum(
        all(l + k <= 5 for l, k in zip(lock, key))
        for lock, key in itertools.product(locks, keys)
    )

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    blocks = data_src.read().split('\n\n')
    keys = []
    locks = []
    for block in blocks:
        lines = block.splitlines()
        pins = [0]*5
        for line in lines[1:-1]:
            for c, ch in enumerate(line):
                pins[c] += ch == '#'

        if lines[0] == '#####':
            locks.append(pins)
        else:
            keys.append(pins)

    return [locks, keys]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=3338)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
    TEST_ANSWER1 = 3

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float('nan')

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
