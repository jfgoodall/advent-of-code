#!/usr/bin/env python3
import time
import typing
from io import StringIO

import numpy as np


def part1(banks):
    total = 0
    for bank in banks:
        idx1 = np.argmax(bank[:-1])
        idx2 = np.argmax(bank[idx1+1:]) + idx1 + 1
        total += bank[idx1] * 10 + bank[idx2]
    return total

def part2(banks):
    total = 0
    for bank in banks:
        joltage = 0
        for digit in range(11, -1, -1):
            check_digits = bank[:-digit] if digit else bank
            idx = np.argmax(check_digits)
            joltage = joltage * 10 + bank[idx]
            bank = bank[idx+1:]
        total += joltage
    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    data = []
    for line in data_src.read().splitlines():
        data.append(tuple(int(x) for x in line))
    return [data]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=17359)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=172787336861064)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()
    TEST_ANSWER1 = 357

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 3121910778619

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
