#!/usr/bin/env python3

def solve_part1(entries):
    # entries: [(min, max, char, pw), ...]
    # returns # of valid entries
    from collections import Counter
    valid = 0
    for min_count, max_count, char, password in entries:
        counter = Counter(password)
        if min_count <= counter[char] <= max_count:
            valid += 1
    return valid

def solve_part2(entries):
    # entries: [(idx1, idx2, char, pw), ...]
    # returns # of valid entries
    valid = 0
    for idx1, idx2, char, password in entries:
        match1 = password[idx1-1] == char
        match2 = password[idx2-1] == char
        if (match1 and not match2) or (not match1 and match2):
            valid += 1
    return valid

def test_solve():
    test_input = [(1, 3, 'a', 'abcde'), (1, 3, 'b', 'cdefg'), (2, 9, 'c', 'ccccccccc')]
    assert solve_part1(test_input) == 2
    assert solve_part2(test_input) == 1

if __name__ == '__main__':
    test_solve()
    with open('day02-input.dat') as infile:
        import re
        entries = [re.split('\W+', line) for line in infile]
        entries = list(map(lambda x: (int(x[0]), int(x[1]), x[2], x[3]), entries))
    print(f"Part 1: {solve_part1(entries)}")
    print(f"Part 2: {solve_part2(entries)}")
