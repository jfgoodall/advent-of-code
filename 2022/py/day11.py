#!/usr/bin/env python3
from __future__ import annotations

import functools
import operator
import time
from dataclasses import dataclass
from io import StringIO


@dataclass
class Monkey:
    items: list[int]
    op: Callable
    test: int
    targets: tuple[int]
    inspections: int = 0

def part1(monkeys):
    for _ in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.op(item) // 3
                if item % monkey.test == 0:
                    monkeys[monkey.targets[0]].items.append(item)
                else:
                    monkeys[monkey.targets[1]].items.append(item)
            monkey.inspections += len(monkey.items)
            monkey.items.clear()

    inspections = sorted(m.inspections for m in monkeys)
    return inspections[-1] * inspections[-2]

def part2(monkeys):
    # this should produce a safe upper bound for any item, preventing item
    # size from growing out of control
    max_item_size = functools.reduce(operator.mul, (m.test for m in monkeys))

    for _ in range(10000):
        for idx, monkey in enumerate(monkeys):
            for item in monkey.items:
                item = monkey.op(item) % max_item_size  # limit item size
                if item % monkey.test == 0:
                    monkeys[monkey.targets[0]].items.append(item)
                else:
                    monkeys[monkey.targets[1]].items.append(item)
            monkey.inspections += len(monkey.items)
            monkey.items.clear()

    inspections = sorted(m.inspections for m in monkeys)
    return inspections[-1] * inspections[-2]

def parse_input(data_src):
    def trailing_int(s):
        return int(s.split()[-1])

    data_src.seek(0)
    monkeys = []
    for block in data_src.read().split('\n\n'):
        block = block.splitlines()
        items = [int(val.strip(',')) for val in block[1].split()[2:]]
        op_val = block[2].split()[-2:]
        assert op_val[0] in '*+'
        if op_val[0] == '*':
            if op_val[1] == 'old':
                op = lambda x: x*x
            else:
                op = functools.partial(operator.mul, int(op_val[1]))
        else:  # op_val[0] == '+'
            op = functools.partial(operator.add, int(op_val[1]))
        test = trailing_int(block[3])
        targets = trailing_int(block[4]), trailing_int(block[5])
        monkeys.append(Monkey(items, op, test, targets))
    return monkeys

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(parse_input(test_data)) == test_answers[0]
        print_result('1', part1, parse_input(infile))  # 67830

        assert part2(parse_input(test_data)) == test_answers[1]
        print_result('2', part2, parse_input(infile))  # 15305381442

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (10605, 2713310158)
    TEST_INPUT = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
