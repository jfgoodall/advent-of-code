#!/usr/bin/env python3
import functools
import itertools
import math
import os
import re
import sys
import time
import typing
from collections import Counter, defaultdict, namedtuple
from dataclasses import dataclass
from enum import Enum, IntEnum
from functools import cache
from io import StringIO
from pprint import pprint

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable


def part1(parsed):
    pass

def part2(parsed):
    pass

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    head, *body = data_src.read().splitlines()
    for line in data_src.read().splitlines():
        pass
    return [data_src.read().splitlines()]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # -

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # -

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
data
"""
    TEST_ANSWER1 = float('nan')

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float('nan')

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
