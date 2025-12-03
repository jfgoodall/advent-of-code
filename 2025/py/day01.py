#!/usr/bin/env python3
import time
import typing
from io import StringIO


def part1(turns):
    zeros = 0
    pos = 50
    for dir, count in turns:
        if dir == 'L':
            count = -count
        pos += count
        if pos % 100 == 0:
            zeros += 1
    return zeros

def part2(turns):
    zeros = 0
    pos = 50
    for dir, count in turns:
        spins, count = divmod(count, 100)
        zeros += spins
        if dir == 'L':
            newpos = (pos - count) % 100
            if pos:
                zeros += int(newpos == 0 or newpos > pos)
        else:
            newpos = (pos + count) % 100
            zeros += int(newpos < pos)
        pos = newpos
    return zeros

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    data = []
    for line in data_src.read().splitlines():
        data.append((line[0], int(line[1:])))
    return [data]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=None)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=None)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
    TEST_ANSWER1 = 3

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 6

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
