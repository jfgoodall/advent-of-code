#!/usr/bin/env python3
import math
import time
import typing
from io import StringIO

OPERATION_MAP = {
    '+': sum,
    '*': math.prod
}

def part1(data):
    data = [line.split() for line in data]
    total = 0
    for col in range(len(data[0])):
        op = data[-1][col]
        total += OPERATION_MAP[op](int(data[i][col]) for i in range(len(data) - 1))
    return total

def part2(data):
    ops = data[-1].split()
    data = data[:-1]

    total = 0
    start_idx = 0
    end_idx = 0
    for op in ops:
        while (
            end_idx < len(data[0]) and
            any(data[row][end_idx] != ' ' for row in range(len(data)))
        ):
            end_idx += 1

        nums = [0] * (end_idx - start_idx)
        for i in range(start_idx, end_idx):
            for row in range(len(data)):
                if data[row][i] != ' ':
                    nums[i-start_idx] *= 10
                    nums[i-start_idx] += int(data[row][i])

        end_idx += 1
        start_idx = end_idx

        total += OPERATION_MAP[op](nums)

    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read().splitlines()]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=6605396225322)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=11052310600986)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  "
    TEST_ANSWER1 = 4277556

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 3263827

    return (
        (StringIO(TEST_INPUT1), TEST_ANSWER1),
        (StringIO(TEST_INPUT2), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
