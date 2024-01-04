#!/usr/bin/env python3
import itertools
import math
import time
from collections import deque
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

class MonadError(Exception):
    pass

""" This problem is not a puzzle you write a program to solve. It's to test
    your ability to read code and reason out its logic. All the code below is
    a worthless attempt to figure out the answer programmatically, but really
    it's a pen and paper exercise. I don't like it.
"""
"""
1  div z 1    8  div z 26     [1] - 16 + 15 = [8]
   add x 12      add x -16    [1] - 1 = [8]
   add y 15      add y 15

2  div z 1    5  div z 26     [2] - 7 + 12 = [5]
   add x 14      add x -7     [2] + 5 = [5]
   add y 12      add y 15

3  div z 1    4  div z 26     [3] - 9 + 15 = [4]
   add x 11      add x -9     [3] + 6 = [4]
   add y 15      add y 12

6  div z 1    7  div z 26     [6] - 1 + 2 = [7]
   add x 11      add x -1     [6] + 1 = [7]
   add y 2       add y 11

9  div z 1    10 div z 26     [9] - 15 + 10 = [10]
   add x 11      add x -15    [9] - 5 = [10]
   add y 10      add y 2

11 div z 1    14 div z 26     [11] - 0 + 0 = [14]
   add x 10      add x 0      [11] = [14]
   add y 0       add y 15

12 div z 1    13 div z 26     [12] - 4 + 0 = [13]
   add x 12      add x -4     [12] - 4 = [13]
   add y 0       add y 15

Digit : 123456789abced
Max   : 94399898949959
Min   : 21176121611511
"""

class Monad:
    def __init__(self, instr):
        self._instr = instr
        self._registers = [0, 0, 0, 0]  # w, x, y, z

    def validate_model_no(self, inp):
        """inp is list of 14 integers"""
        self._validate_input(inp)
        # self._reset()
        inp = deque(inp)

        for instr in self._instr:
            operator, *operands = instr.split()
            out_idx = self._get_register_idx(operands[0])

            if operator == 'inp':
                self._registers[out_idx] = inp.popleft()
                continue

            a = self._get_operand_value(operands[0])
            b = self._get_operand_value(operands[1])
            if operator == 'add':
                self._registers[out_idx] = a + b
            elif operator == 'mul':
                self._registers[out_idx] = a * b
            elif operator == 'div':
                if b == 0:
                    raise MonadError
                self._registers[out_idx] = math.trunc(a/b)
            elif operator == 'mod':
                if a < 0 or b <= 0:
                    raise MonadError
                self._registers[out_idx] = a % b
            elif operator == 'eql':
                self._registers[out_idx] = int(a == b)
        return self._registers[3] == 0


    def _reset(self):
        self._registers = [0, 0, 0, 0]

    def _validate_input(self, inp):
        for i in inp:
            if i == 0:
                raise ValueError

    def _get_register_idx(self, reg):
        return 'wxyz'.index(reg)

    def _get_operand_value(self, op):
        if op in 'wxyz':
            return self._registers[self._get_register_idx(op)]
        return int(op)

def part1(instr):
    ndigits = 3
    # instr = instr[-18*ndigits:]
    instr = instr[:18*ndigits]
    alu = Monad(instr)
    try:
        for inp in itertools.product(range(9, 0, -1), repeat=len(instr)//18):
            alu._reset()
            # for z in range(26):
            #     alu._registers[3] = z
            #     if alu.validate_model_no(list(inp)):
            #         print(z, ''.join(map(str, inp)))
            valid = alu.validate_model_no(list(inp))
            print(alu._registers[3])
            if valid:
                print(''.join(map(str, inp)))
                # return ''.join(map(str, inp))
    except MonadError:
        print(f'MonadError: {inp}')

def part2(parsed):
    pass

def parse_input(data_src):
    data_src.seek(0)
    return [line.strip() for line in data_src]

def run_tests():
    TEST_INPUT = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""
    test_data = StringIO(TEST_INPUT.strip())
    alu = Monad(parse_input(test_data))
    for inp in range(0, 10):
        try:
            alu._reset()
            alu.validate_model_no([inp])
            assert int(''.join(map(str, alu._registers)), 2) == inp
        except ValueError:
            assert inp == 0

    TEST_INPUT = """
inp z
inp x
mul z 3
eql z x
"""
    test_data = StringIO(TEST_INPUT.strip())
    alu = Monad(parse_input(test_data))
    for inp in itertools.product(range(1, 10), range(1, 10)):
        alu.validate_model_no(list(inp))
        assert alu._registers[3] == 1 or inp[0]*3 != inp[1]

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    print('Part 1: 94399898949959')  # dumb
    print('Part 2: 21176121611511')  # dumb

"""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y

x = (z % 26 + 12) == w) == 0  ; x = {0,1}
z = z * (25 * x + 1) + (w + 15 * x)

inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

x = z % 26
x = ((z % 26)/1 + 12) == w) == 0  ; x = {0,1}
z = z * (25 * x + 1) + ((w + 15) * x)

inp w
mul x 0
add x z
mod x 26  x=z%26
div z 26  z/=26
add x 0
eql x w   x==w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x   x:{0}
add z y   y:{0}
"""
