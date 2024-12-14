#!/usr/bin/env python3
import re
import time
import typing
from io import StringIO


def calc_tokens(dxa, dya, dxb, dyb, px, py, limit=float('inf'), prize_bias=0):
    """
        1) A*dxa + B*dxb = px
           A = (px - B*dxb) / dxa

        2) A*dya + B*dyb = py
           (px - B*dxb) * dya / dxa + B*dyb = py
           px*dya - B*dxb*dya + B*dyb*dxa = py*dxa
           B*dyb*dxa - B*dxb*dya = py*dxa - dya*px
           B * (dyb*dxa - dxb*dya) = py*dxa - dya*px
           B = (py*dxa - dya*px) / (dyb*dxa - dxb*dya)
    """
    px += prize_bias
    py += prize_bias

    b = (py*dxa - px*dya) // (dyb*dxa - dxb*dya)
    a = (px - b*dxb) // dxa

    if (
        a*dxa + b*dxb == px and
        a*dya + b*dyb == py and
        a <= limit and b <= limit
    ):
        return 3*a + b
    return 0

def part1(machines):
    return sum(calc_tokens(*a, *b, *p, limit=100) for a, b, p in machines)

def part2(machines):
    return sum(
        calc_tokens(*a, *b, *p, prize_bias=10000000000000)
        for a, b, p in machines
    )

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    BUTTON_RE = re.compile(r'Button [AB]: X\+(\d+), Y\+(\d+)')
    PRIZE_RE = re.compile(r'Prize: X=(\d+), Y=(\d+)')
    REGEXES = (BUTTON_RE, BUTTON_RE, PRIZE_RE)

    data_src.seek(0)

    # "one" liner
    return [tuple(
        tuple(
            map(int, regex.match(line).groups())
            for regex, line
            in zip(REGEXES, machine.splitlines())
        )
        for machine in data_src.read().split('\n\n')
    )]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 33921

        # no test answer provided for part 2
        solve_part('2', part2, *parse_input(infile))  # 82261957837868

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
    TEST_ANSWER1 = 480

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float('nan')

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
