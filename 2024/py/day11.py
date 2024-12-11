#!/usr/bin/env python3
import math
import time
import typing
from functools import lru_cache
from io import StringIO


@lru_cache(maxsize=None)
def blink(number, cycles):
    if cycles == 0:
        return 1
    elif number == 0:
        return blink(1, cycles-1)
    elif (num_digits := int(math.log(number, 10)) + 1) % 2 == 0:
        num1, num2 = divmod(number, 10**(num_digits/2))
        return blink(int(num1), cycles-1) + blink(int(num2), cycles-1)
    else:
        return blink(number*2024, cycles-1)

def part1(stones):
    return sum(blink(st, 25) for st in stones)

def part2(stones):
    return sum(blink(st, 75) for st in stones)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [list(map(int, data_src.read().strip().split()))]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 194782

        # no test answer provided for part 2
        solve_part('2', part2, *parse_input(infile))  # 233007586663131

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
125 17
"""
    TEST_ANSWER1 = 55312

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float('nan')

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
