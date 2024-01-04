#!/usr/bin/env python3

def transform(value, subject_num):
    value *= subject_num
    return value % 20201227

def find_loop_size(key):
    loop_size = 0
    value = 1
    while True:
        loop_size += 1
        value = transform(value, 7)
        if value == key:
            return loop_size

def part1(public_keys: tuple):
    loop_size = find_loop_size(public_keys[0])
    value = 1
    for _ in range(loop_size):
        value = transform(value, public_keys[1])
    return value

def run_tests():
    assert find_loop_size(5764801) == 8
    assert find_loop_size(17807724) == 11
    assert part1((5764801, 17807724)) == 14897079

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    public_keys = tuple(map(int, test_input))
    print(f"Part 1: {part1(public_keys)}")
