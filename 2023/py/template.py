#!/usr/bin/env python3
from __future__ import annotations

import functools
import itertools
import os
import re
import sys
import time
from collections import Counter, defaultdict, namedtuple
from dataclasses import dataclass
from enum import Enum, IntEnum
from functools import lru_cache
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

def parse_input(data_src):
    data_src.seek(0)
    head, *body = data_src.read().splitlines()
    for line in data_src.read().splitlines():
        pass
    return [data_src.read().splitlines()]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # -

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (0, 0)
    TEST_INPUT = """
test data
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
