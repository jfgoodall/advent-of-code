#!/usr/bin/env python3
import time
from io import StringIO

STR_TO_NUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
}
STR_TO_NUM_R = {k[::-1]: v for k, v in STR_TO_NUM.items()}

def find_first_num(s, mapping=None):
    for i, c in enumerate(s):
        if c.isnumeric():
            return int(c)
        if mapping:
            for strnum, num in mapping.items():
                if s[i:].startswith(strnum):
                    return num

def part1(parsed):
    return sum(10*find_first_num(line) + find_first_num(line[::-1])
               for line in parsed)

def part2(parsed):
    return sum(10*find_first_num(line, STR_TO_NUM) +
                  find_first_num(line[::-1], STR_TO_NUM_R)
               for line in parsed)

def parse_input(data_src):
    data_src.seek(0)
    return [data_src.read().splitlines()]

def main():
    with open(__file__[:-3] + '-input.dat') as infile:
        test_data, test_answers = get_test_data()
        assert part1(*parse_input(test_data)) == test_answers
        print_result('1', part1, *parse_input(infile))  # -

        test_data, test_answers = get_test_data2()
        assert part2(*parse_input(test_data)) == test_answers
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = 142
    TEST_INPUT = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

def get_test_data2():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = 281
    TEST_INPUT = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
