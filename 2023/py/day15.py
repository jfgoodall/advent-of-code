#!/usr/bin/env python3
import functools
import time
from collections import defaultdict
from io import StringIO


def aoc_hash(s):
    return functools.reduce(lambda val, ch: (val + ord(ch)) * 17 % 256, s, 0)

def part1(strings):
    return sum(aoc_hash(s) for s in strings)

def part2(strings):
    counter = 0
    hashmap = defaultdict(dict)
    for s in strings:
        if s[-1] == '-':
            label = s[:-1]
            hashmap[aoc_hash(label)].pop(label, None)
        else:
            label, focal_len = s.split('=')
            key = aoc_hash(label)
            lens = hashmap[key].get(label)
            if lens:
                hashmap[key][label] = (lens[0], focal_len)
            else:
                hashmap[key][label] = (counter, focal_len)
                counter += 1

    total = 0
    for box, lenses in hashmap.items():
        for slot, lens in enumerate(sorted(lenses.values())):
            total += (box+1) * (slot+1) * int(lens[1])
    return total

def parse_input(data_src):
    data_src.seek(0)
    return [data_src.read().strip().split(',')]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 516070

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 244981

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (1320, 145)
    TEST_INPUT = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
