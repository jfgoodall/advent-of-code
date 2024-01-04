#!/usr/bin/env python3
import time, itertools, functools, hashlib
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def search_hashes(secret, zeros):
    for result in itertools.count(1):
        s = (secret+str(result)).encode('utf-8')
        if hashlib.md5(s).hexdigest().startswith('0'*zeros):
            return result

def part1(secret):
    return search_hashes(secret, 5)

def part2(secret):
    return search_hashes(secret, 6)

def run_tests():
    assert part1('abcdef') == 609043

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    print_result('1', part1, 'iwrupvqb')  # 346386
    print_result('2', part2, 'iwrupvqb')  # 9958218
