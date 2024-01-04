#!/usr/bin/env python3

def solve(entries, nelem, total=2020):
    from itertools import combinations
    from functools import reduce
    for elems in combinations(entries, nelem):
        if sum(elems) == total:
            return reduce(lambda x, y: x*y, elems)

def test_solve():
    test_input = [1721, 979, 366, 299, 675, 1456]
    assert solve(test_input, 2) == 514579
    assert solve(test_input, 3) == 241861950

if __name__ == '__main__':
    test_solve()
    with open('day01-input.dat') as infile:
        entries = [int(line.strip()) for line in infile]
    print(f"Part 1: {solve(entries, 2)}")
    print(f"Part 2: {solve(entries, 3)}")
