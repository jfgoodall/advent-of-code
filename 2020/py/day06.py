#!/usr/bin/env python3
from functools import reduce

def solve_part1(lines):
    groups = [set(entry.replace('\n', '')) for entry in lines.split('\n\n')]
    return reduce(lambda total, group: total+len(group), groups, 0)

def solve_part2(lines):
    groups = [[set(line) for line in entry.split('\n')] for entry in lines.split('\n\n')]
    return reduce(lambda total, group: total+len(set.intersection(*group)), groups, 0)

def test_solve():
    test_input = """
abc

a
b
c

ab
ac

a
a
a
a

b
""".strip()
    assert solve_part1(test_input) == 11
    assert solve_part2(test_input) == 6

if __name__ == '__main__':
    test_solve()
    with open('day06-input.dat') as infile:
        lines = infile.read().strip()
    print(f"Part 1: {solve_part1(lines)}")
    print(f"Part 2: {solve_part2(lines)}")
