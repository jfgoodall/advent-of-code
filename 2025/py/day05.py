#!/usr/bin/env python3
import time
import typing
from io import StringIO


def consolidate_ranges(ranges):
    ranges = sorted(ranges)
    idx = 0
    while True:
        if idx == len(ranges) - 1:
            break

        if (
            ranges[idx+1][0] <= ranges[idx][1] <= ranges[idx+1][1] or
            ranges[idx][0] <= ranges[idx+1][1] <= ranges[idx][1]
        ):
            ranges[idx][1] = max(ranges[idx][1], ranges[idx+1][1])
            del ranges[idx+1]
        else:
            idx += 1

    return ranges

def part1(fresh, ingredients):
    fresh = consolidate_ranges(fresh)
    total = 0
    for ingred in ingredients:
        for a, b in fresh:
            if a <= ingred <= b:
                total += 1
                break
    return total

def part2(fresh, _):
    fresh = consolidate_ranges(fresh)
    total = 0
    for a, b in fresh:
        total += b - a + 1
    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    fresh, ingredients = data_src.read().split('\n\n')
    fresh = [list(map(int, line.split('-'))) for line in fresh.splitlines()]
    ingredients = [int(i) for i in ingredients.splitlines()]
    return [fresh, ingredients]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=638)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=352946349407338)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
    TEST_ANSWER1 = 3

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 14

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
