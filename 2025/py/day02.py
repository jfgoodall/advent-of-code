#!/usr/bin/env python3
import time
import typing
from io import StringIO


def part1(ranges):
    invalid_ids = set()
    for small, large in ranges:
        sm_int = int(small)
        lg_int = int(large)
        digits = (len(small)+1)//2
        min_check = small[:digits] if len(small) == digits * 2 else '1'+'0'*(digits-1)
        max_check = large[:digits] if len(large) == digits * 2 else '9'*digits
        for test_id in range(int(min_check), int(max_check)+1):
            test_num = int(str(test_id)*2)
            if test_num >= sm_int and test_num <= lg_int:
                invalid_ids.add(test_num)
    return sum(invalid_ids)

def part2(ranges):
    invalid_ids = set()
    for small, large in ranges:
        sm_int = int(small)
        lg_int = int(large)
        for digits in range(1, (len(small)+1)//2+1):
            for rep in range(max(2, len(small)//digits), len(large)//digits+1):
                min_check = small[:digits] if len(small) == digits * rep else '1'+'0'*(digits-1)
                max_check = large[:digits] if len(large) == digits * rep else '9'*digits
                for test_id in range(int(min_check), int(max_check)+1):
                    test_num = int(str(test_id)*rep)
                    if test_num >= sm_int and test_num <= lg_int:
                        invalid_ids.add(test_num)
    return sum(invalid_ids)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    data = []
    for entries in data_src.read().strip().split(','):
        data.append(tuple(entries.split('-')))
    return [data]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=38158151648)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=45283684555)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""
    TEST_ANSWER1 = 1227775554

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 4174379265

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
