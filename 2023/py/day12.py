#!/usr/bin/env python3
from __future__ import annotations

import multiprocessing
import time
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

# sys.path.append(os.path.dirname(__file__))
# from common_patterns.point import Point2D
# from common_patterns.itertools import pairwise


def valid_arrangement(arr, groups):
    return [len(x) for x in ''.join(arr).split()] == groups

def count_arrangements(arr, groups):
    indices = [i for i, x in enumerate(arr) if x == '?']
    total = 0
    for c in range(2**len(indices)):
        for bit_pos, idx in enumerate(indices):
            arr[idx] = '#' if c & (1 << bit_pos) else ' '
        if valid_arrangement(arr, groups):
            total += 1
    return total

def part1(springs):
    total = 0
    for arr, groups in tqdm(springs):
        total += count_arrangements(arr, groups)
    return total

def part2_lol_no(springs):
    total = 0
    for arr, groups in tqdm(springs):
        big_arr = '?'.join([''.join(arr)]*5)
        total += count_arrangements(list(big_arr), groups*5)
    return total

def valid_partial(arr, groups):
    group_idx = 0
    arr_idx = 0
    while arr_idx < len(arr):
        if arr[arr_idx] == '?':
            return True
        elif arr[arr_idx] == ' ':
            arr_idx += 1
        else:
            if group_idx == len(groups):
                return False

            l = 0
            while arr_idx < len(arr) and arr[arr_idx] == '#':
                arr_idx += 1
                l += 1

            if arr_idx == len(arr):
                if group_idx != len(groups)-1:
                    return False
            elif l > groups[group_idx] or arr[arr_idx] == ' ' and l != groups[group_idx]:
                return False

            group_idx += 1
    return valid_arrangement(arr, groups)

# def recurse_arrangements(arr, groups):
def recurse_arrangements(springs):
    arr, groups = springs
    indices = [i for i, x in enumerate(arr) if x == '?']

    def dfs(arr, i):
        if i == len(indices):
            return 1

        total = 0
        a1 = arr.copy()
        a1[indices[i]] = ' '
        if valid_partial(a1, groups):
            total += dfs(a1, i+1)

        a2 = arr.copy()
        a2[indices[i]] = '#'
        if valid_partial(a2, groups):
            total += dfs(a2, i+1)
        return total

    return dfs(arr, 0)

def part2(springs):
    pool = multiprocessing.Pool(7)
    big_springs = [[list('?'.join([''.join(arr)] * 5)), groups*5] for arr, groups in springs]
    return sum(pool.map(recurse_arrangements, big_springs))

def parse_input(data_src):
    data_src.seek(0)
    springs = []
    for line in data_src.read().splitlines():
        arr, groups = line.split()
        springs.append([list(arr.replace('.', ' ')), list(map(int, groups.split(',')))])
    return [springs]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        # assert part1(*parse_input(test_data)) == test_answers[0]
        # print_result('1', part1, *parse_input(infile))  # 7506

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (21, 525152)
    TEST_INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
