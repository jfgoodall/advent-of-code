#!/usr/bin/env python3
import time
import typing
from functools import cache
from io import StringIO


@cache
def pattern_combos(pattern, towels):
    combos = 0
    for towel in towels:
        if towel == pattern:
            combos += 1
        elif pattern.startswith(towel):
            combos += pattern_combos(pattern[len(towel):], towels)
    return combos

def part1(towels, patterns):
    return sum(pattern_combos(p, towels) > 0 for p in patterns)

def part2(towels, patterns):
    return sum(pattern_combos(p, towels) for p in patterns)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    towels, patterns = data_src.read().split('\n\n')
    towels = tuple(map(str.strip, towels.split(',')))
    patterns = patterns.splitlines()
    return [towels, patterns]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 228

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 584553405070389

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
    TEST_ANSWER1 = 6

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 16

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
