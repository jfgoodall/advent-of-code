#!/usr/bin/env python3
import re
import time
from io import StringIO


def part1(stacks, moves):
    for count, frm, to in moves:
        boxes = reversed(stacks[frm][-count:])
        stacks[to].extend(boxes)
        del stacks[frm][-count:]
    return ''.join(stack[-1] for stack in stacks)

def part2(stacks, moves):
    for count, frm, to in moves:
        boxes = stacks[frm][-count:]
        stacks[to].extend(boxes)
        del stacks[frm][-count:]
    return ''.join(stack[-1] for stack in stacks)

def parse_input(data_src):
    data_src.seek(0)
    initial, instructions = data_src.read().split('\n\n')

    # pre-commit doesn't like trailing whitespace in the test input string
    # below or in the input file; make the parsing work with or without them
    initial = initial.splitlines()
    num_stacks = int(initial[-1].split()[-1])
    stacks = [[] for _ in range(num_stacks)]
    for line in reversed(initial[:-1]):
        for idx, stack in enumerate(stacks):
            col = idx*4+1
            if col >= len(line):
                break
            if line[col] != ' ':
                stack.append(line[col])

    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    moves = []
    for instr in instructions.strip().splitlines():
        count, frm, to = map(int, pattern.match(instr).groups())
        moves.append((count, frm-1, to-1))
    return stacks, moves

def run_tests():
    TEST_INPUT = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    test_data = StringIO(TEST_INPUT)
    assert part1(*parse_input(test_data)) == 'CMZ'
    assert part2(*parse_input(test_data)) == 'MCD'

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, *parse_input(infile))  # QNNTGTPFN
        print_result('2', part2, *parse_input(infile))  # GGNPJBTTR
