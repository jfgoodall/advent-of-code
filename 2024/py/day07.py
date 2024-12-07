#!/usr/bin/env python3
import itertools
import time
import typing
from io import StringIO


def part1(data):
    answer = 0
    for total, operands in data:
        ops_possibilities = itertools.product('+*', repeat=len(operands)-1)
        for ops_combo in ops_possibilities:
            res = operands[0]
            for operator, operand in zip(ops_combo, operands[1:]):
                match operator:
                    case '+':
                        res += operand
                    case '*':
                        res *= operand
                if res > total: break
            if res == total:
                answer += total
                break

    return answer

def part2(data):
    answer = 0
    for total, operands in data:
        ops_possibilities = itertools.product('+*|', repeat=len(operands)-1)
        for ops_combo in ops_possibilities:
            res = operands[0]
            for operator, operand in zip(ops_combo, operands[1:]):
                match operator:
                    case '+':
                        res += operand
                    case '*':
                        res *= operand
                    case '|':
                        res = int(str(res) + str(operand))
                if res > total: break
            if res == total:
                answer += total
                break

    return answer

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    data = []
    for line in data_src.read().splitlines():
        total, operands = line.split(':')
        operands = operands.split()
        data.append((int(total), tuple(map(int, operands))))
    return [data]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 7710205485870

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 20928985450275

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
    TEST_ANSWER1 = 3749

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 11387

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()