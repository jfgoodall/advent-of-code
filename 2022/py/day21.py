#!/usr/bin/env python3
import operator
import re
import time
from io import StringIO


def resolve(monkeys, label):
    val = monkeys[label]
    if len(val) == 1:
        return val[0]
    arg1 = resolve(monkeys, val[0])
    arg2 = resolve(monkeys, val[1])
    return val[2](arg1, arg2)

def dependencies(monkeys, label):
    val = monkeys[label]
    if len(val) == 1:
        return set((label,))
    arg1 = dependencies(monkeys, val[0])
    arg2 = dependencies(monkeys, val[1])
    return arg1 | arg2

def part1(monkeys):
    return resolve(monkeys, 'root')

def part2(monkeys):
    root = 'root'
    left = dependencies(monkeys, monkeys[root][0])
    right = dependencies(monkeys, monkeys[root][1])
    assert not ('humn' in left and 'humn' in right)

    if 'humn' in left:
        target = resolve(monkeys, monkeys[root][1])
        root = monkeys['root'][0]
    else:
        target = resolve(monkeys, monkeys[root][0])
        root = monkeys['root'][1]

    while root != 'humn':
        left = dependencies(monkeys, monkeys[root][0])
        right = dependencies(monkeys, monkeys[root][1])
        assert not ('humn' in left and 'humn' in right)

        # reverse the expression to solve for the variable
        if 'humn' in left:  # solve for left operand
            if monkeys[root][3] == '+':
                target -= resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '-':
                target += resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '*':
                target //= resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '/':
                target *= resolve(monkeys, monkeys[root][1])
            root = monkeys[root][0]
        else:  # solve for right operand
            if monkeys[root][3] == '+':
                target -= resolve(monkeys, monkeys[root][0])
            elif monkeys[root][3] == '-':
                target = resolve(monkeys, monkeys[root][0]) - target
            elif monkeys[root][3] == '*':
                target //= resolve(monkeys, monkeys[root][0])
            elif monkeys[root][3] == '/':
                target = resolve(monkeys, monkeys[root][0]) // target
            root = monkeys[root][1]
    return target

def parse_input(data_src):
    data_src.seek(0)
    MONKEY_VAL_RE = re.compile(r'(\w{4}): (\d+)')
    MONKEY_OP_RE = re.compile(r'(\w{4}): (\w{4}) ([-+*/]) (\w{4})')
    monkeys = {}
    for line in data_src.read().splitlines():
        if m := MONKEY_VAL_RE.match(line):
            label, val = m.groups()
            monkeys[label] = (int(val),)
        elif m := MONKEY_OP_RE.match(line):
            label, arg1, op, arg2 = m.groups()
            op_fn = {'+': operator.add, '-': operator.sub,
                     '*': operator.mul, '/': operator.floordiv}[op]
            monkeys[label] = (arg1, arg2, op_fn, op)
        else:
            assert False
    return [monkeys]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 81075092088442

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 3349136384441

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (152, 301)
    TEST_INPUT = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
