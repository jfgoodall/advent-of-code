#!/usr/bin/env python3
import re
import time
import typing
from io import StringIO


def part1(memory):
    nums = re.findall(r'mul\((\d+),(\d+)\)', memory)
    return sum(int(a) * int(b) for a, b in nums)

def part2(memory):
    instrs = re.findall(r"""
        mul\(\d+,\d+\)
        |
        do(?:n't)?\(\)
        """,
        memory, re.X
    )

    total = 0
    enabled = True
    for instr in instrs:
        match instr.strip('()').replace('(', ',').split(','):
            case ["mul", a, b] if enabled:
                total += int(a) * int(b)
            case ["do"]:
                enabled = True
            case ["don't"]:
                enabled = False

    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read()]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test1_data)) == test1_answer
        solve_part('1', part1, *parse_input(infile))  # 157621318

        assert part2(*parse_input(test2_data)) == test2_answer
        solve_part('2', part2, *parse_input(infile))  # 79845780

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[(tuple[str, str|float],) * 2]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
    TEST_ANSWER1 = 161

    TEST_INPUT2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
    TEST_ANSWER2 = 48

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
