#!/usr/bin/env python3
from enum import Enum

def validate(numbers, idx, preamble):
    from itertools import combinations
    assert idx >= preamble and idx < len(numbers)
    for combo in combinations(numbers[idx-preamble:idx], 2):
        if sum(combo) == numbers[idx]:
            return True
    return False

def find_first_invalid(numbers, preamble):
    for idx in range(preamble, len(numbers)):
        if not validate(numbers, idx, preamble):
            return numbers[idx]

def find_target_range(numbers, target_sum):
    lower, upper = (0, 1)
    total = numbers[0]
    for lower in range(len(numbers)):
        while total < target_sum:
            total += numbers[upper]
            upper += 1
        if total == target_sum:
            break

        total -= numbers[lower]
        lower += 1

        while total > target_sum:
            upper -= 1
            total -= numbers[upper]
        if total == target_sum:
            break

    return lower, upper

def sum_min_max_of_target_range(numbers, target_sum):
    target_range = find_target_range(numbers, target_sum)
    return min(numbers[target_range[0]:target_range[1]]) + \
           max(numbers[target_range[0]:target_range[1]])

def parse_input(lines):
    return [int(line.strip()) for line in lines]

def test_validate():
    test_input = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""".strip()
    numbers = parse_input(test_input.split('\n'))
    assert find_first_invalid(numbers, 5) == 127
    assert sum_min_max_of_target_range(numbers, 127) == 62

if __name__ == '__main__':
    test_validate()
    with open('day09-input.dat') as infile:
        numbers = parse_input(infile)
    target_sum = find_first_invalid(numbers, 25)
    print(f"Part 1: {target_sum}")
    print(f"Part 2: {sum_min_max_of_target_range(numbers, target_sum)}")
