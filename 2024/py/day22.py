#!/usr/bin/env python3
import time
import typing
from collections import defaultdict
from io import StringIO


def generate_secret(secret):
    secret = ((secret << 6) ^ secret) & 0xFFFFFF
    secret = ((secret >> 5) ^ secret) & 0xFFFFFF
    secret = ((secret << 11) ^ secret) & 0xFFFFFF
    return secret

def part1(secrets):
    total = 0
    for secret in secrets:
        for _ in range(2000):
            secret = generate_secret(secret)
        total += secret
    return total

def part2(secrets):
    sequence_prices = defaultdict(int)
    for secret in secrets:
        seen = set()
        sequence = tuple()
        prev_price = secret % 10

        for _ in range(2000):
            secret = generate_secret(secret)
            price = secret % 10
            sequence = sequence[-3:] + (price - prev_price,)

            if len(sequence) == 4 and sequence not in seen:
                seen.add(sequence)
                sequence_prices[sequence] += price

            prev_price = price

    return max(sequence_prices.values())

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [list(map(int, data_src.read().splitlines()))]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=13022553808)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=1555)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else " ** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms) {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
1
10
100
2024
"""
    TEST_ANSWER1 = 37327623

    TEST_INPUT2 = """
1
2
3
2024
"""
    TEST_ANSWER2 = 23

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
