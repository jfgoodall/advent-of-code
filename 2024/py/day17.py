#!/usr/bin/env python3
import itertools
import time
import typing
from collections import defaultdict
from io import StringIO


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

    2,4: b = a & 111b     ; b in [0..7]
    1,2: b = b ^ 010b     ; b in [0..7]
    7,5: c = a >> b       ; c uses 0..7 lowest bits from a
    0,3: a = a >> 3       ; swallow lowest 3 bits from a
    1,7: b = b ^ 111b     ; b in [0..7]
    4,1: b = b ^ c        ; b influenced by 0..7 lowest bits from a
    5,5: output b & 111b  ; only consider lowest 3 bits of b
    3,0: if a > 0 jmp to beginning

    the lowest 10 bits are hashed to create a 3-bit output; the lowest
    3 bits are dropped and the process repeated
    """

    # create a mapping of all 3-bit outputs from all 10-bit input strings
    hash_bits = 10
    unhash = defaultdict(list)
    for a in range(2**hash_bits):
        output = run_program(a, 0, 0, program)
        unhash[output[0]].append(f'{a:0{hash_bits}b}')

    # work from last output and construct a from most significant bits to least
    valid_a = [
        va for va in unhash[program[-1]]
        if va[:hash_bits-3] == '0'*(hash_bits-3)  # last output only uses 3 hash bits
    ]

    # find the hash strings for each output value such that adjacent strings overlap
    # by 7 bits
    for out_idx in reversed(range(len(program)-1)):
        valid_next_a = []
        for curr_a, next_part in itertools.product(valid_a, unhash[program[out_idx]]):
            if curr_a[-(hash_bits-3):] == next_part[:(hash_bits-3)]:
                valid_next_a.append(curr_a + next_part[-3:])
        valid_a = valid_next_a

    # every a value in valid_a will produce the correct output; return the minimum
    return min(int(va, 2) for va in valid_a)

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
