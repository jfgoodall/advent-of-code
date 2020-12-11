#!/usr/bin/env python3

def solve_part1(lines):
    groups = []
    qs = set()
    for line in lines:
        line = line.strip()
        if not line:
            if qs:
                groups.append(qs)
                qs = set()
        else:
            for c in list(line):
                qs.add(c)
    groups.append(qs)
    total = 0
    for g in groups:
        total += len(g)
    return total

def solve_part2(lines):
    groups = []
    qs = []
    for line in lines:
        line = line.strip()
        if not line:
            if qs:
                groups.append(qs)
                qs = []
        else:
            qs.append(set(list(line)))
    if qs:
        groups.append(qs)
    total = 0
    for g in groups:
        total += len(set.intersection(*g))
    return total

def test_solve():
    test_input = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    assert solve_part1(test_input.split('\n')) == 11
    assert solve_part2(test_input.split('\n')) == 6

if __name__ == '__main__':
    test_solve()
    with open('day06-input.dat') as infile:
        print(f"Part 1: {solve_part1(infile)}")
    with open('day06-input.dat') as infile:
        print(f"Part 2: {solve_part2(infile)}")
