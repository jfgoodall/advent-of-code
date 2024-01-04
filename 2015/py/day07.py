#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def solve_wire(instr, goal, wires=None):
    def get_value(token):
        try:
            return np.array([int(token)], dtype=np.uint16)
        except ValueError:
            try:
                return wires[token]
            except KeyError:
                return solve_wire(instr, token, wires)

    if wires is None:
        wires = {}
    expr = instr[goal]
    if len(expr) == 1:
        wires[goal] = get_value(expr[0])
    elif len(expr) == 2:
        wires[goal] = ~get_value(expr[1])
    elif expr[1] == 'AND':
        wires[goal] = get_value(expr[0]) & get_value(expr[2])
    elif expr[1] == 'OR':
        wires[goal] = get_value(expr[0]) | get_value(expr[2])
    elif expr[1] == 'LSHIFT':
        wires[goal] = get_value(expr[0]) << get_value(expr[2])
    elif expr[1] == 'RSHIFT':
        wires[goal] = get_value(expr[0]) >> get_value(expr[2])
    return wires[goal]

def part1(instr):
    return solve_wire(instr, 'a')

def part2(instr):
    instr['b'] = solve_wire(instr, 'a')
    return solve_wire(instr, 'a')

def parse_input(data_src):
    data_src.seek(0)
    instr = {}
    for line in data_src:
        expr, wire = line.split('->')
        instr[wire.strip()] = expr.split()
    return instr

def run_tests():
    TEST_INPUT = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""
    test_data = StringIO(TEST_INPUT.strip())
    # print(parse_input(test_data))

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 46065
        print_result('2', part2, parse_input(infile))  # 14134
