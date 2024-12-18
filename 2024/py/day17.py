#!/usr/bin/env python3
import time
import typing
from collections import defaultdict
from io import StringIO
from pprint import pprint


def combo_operand_value(operand, a, b, c):
    assert operand != 7
    if 0 <=  operand <= 3:
        return operand
    return (a, b, c)[operand-4]

def run_program(a, b, c, program):
    assert len(program) % 2 == 0

    output = []
    ip = 0
    while ip < len(program):
        opcode, operand = program[ip:ip+2]
        ip += 2
        match opcode:
            case 0:  # adv
                a //= 2 ** combo_operand_value(operand, a, b, c)
            case 1:  # bxl
                b ^= operand
            case 2:  # bst
                b = combo_operand_value(operand, a, b, c) & 0b111
            case 3:  # jnz
                assert operand % 2 == 0
                if a: ip = operand
            case 4:  # bxc
                b ^= c
            case 5:  # out
                output.append(combo_operand_value(operand, a, b, c) & 0b111)
            case 6:  # bdv
                b = a // 2 ** combo_operand_value(operand, a, b, c)
            case 7:  # cdv
                c = a // 2 ** combo_operand_value(operand, a, b, c)
    return output

def part1(a, b, c, program):
    return ','.join(map(str, run_program(a, b, c, program)))

def part2(a, b, c, program):
    """
    Program: 2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0

    2,4: b = a & 111b
    1,2: b = b ^ 010b
    7,5: c = a >> b
    0,3: a = a >> 3
    1,7: b = b ^ 111b
    4,1: b = b ^ c
    5,5: output b & 111b
    3,0: if a > 0 jmp to beginning

    b = a3 ^ 010
    c = (a >> (a3 ^ 010)) ^ 010
    b = a3 ^ 010 ^ 111
      = a3 ^ 101
    b = a3 ^ 101 ^ (a >> (a3 ^ 010)) ^ 010
      = a3 ^ (a >> (a3 ^ 010)) ^ 111

    output b3
    a >>= 3
    loop if a

    the lowest 6 bits are hashed to create a 3-bit output; the lowest
    3 bits are dropped and the process repeated
    """

    # create a mapp
    unhash = defaultdict(list)
    for a in range(0b111111):
        output = run_program(a, 0, 0, program)
        unhash[output[0]].append(a)

    a = 0
    for out in reversed(program):
        a <<= 3
        a |= unhash[out][0]

    print('---')
    pprint(dict(unhash))
    print(program)
    print(run_program(a, 0, 0, program))

    return a

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    lines = data_src.read().splitlines()
    return [
        int(lines[0].split(':')[1]),
        int(lines[1].split(':')[1]),
        int(lines[2].split(':')[1]),
        tuple(map(int, lines[4].split(':')[1].split(',')))
    ]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 7,6,5,3,6,5,7,0,4

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # -

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    TEST_ANSWER1 = "4,6,3,5,6,3,5,2,1,0"

    TEST_INPUT2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
    TEST_ANSWER2 = 117440

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
