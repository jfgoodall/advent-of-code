#!/usr/bin/env python3
import functools
import itertools
import time
import typing
from collections import defaultdict
from io import StringIO


def part1(rules, updates):
    order = defaultdict(set)
    for p1, p2 in rules:
        order[p1].add(p2)

    total = 0
    for update in updates:
        if all(p2 in order[p1] for p1, p2 in itertools.pairwise(update)):
            total += update[len(update)//2]

    return total

def part2(rules, updates):
    order = defaultdict(set)
    for p1, p2 in rules:
        order[p1].add(p2)

    sort_key = functools.cmp_to_key(
        lambda p1, p2: -1 if p2 in order[p1] else 1
    )
    total = 0
    for update in updates:
        if any(p2 not in order[p1] for p1, p2 in itertools.pairwise(update)):
            update.sort(key=sort_key)
            total += update[len(update)//2]

    return total

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    rules_lines, updates_lines = data_src.read().split("\n\n")
    rules = [
        list(map(int, line.split('|'))) for line in rules_lines.splitlines()
    ]
    updates = [
        list(map(int, line.split(','))) for line in updates_lines.splitlines()
    ]
    return [rules, updates]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test1_data)) == test1_answer
        solve_part('1', part1, *parse_input(infile))  # 4637

        assert part2(*parse_input(test2_data)) == test2_answer
        solve_part('2', part2, *parse_input(infile))  # -

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[(str, str|float) * 2]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
    TEST_ANSWER1 = 143

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 123

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
