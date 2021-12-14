#!/usr/bin/env python3
import time, itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def polymerize(template, rules, steps):
    @functools.lru_cache(maxsize=None)
    def expand(pair, step):
        if step == 0:
            return Counter(pair[0])
        return (expand(pair[0]+rules[pair], step-1) +
                expand(rules[pair]+pair[1], step-1))

    expand.cache_clear()  # in case example rules conflict with actual input
    counts = Counter()
    for idx in range(len(template)-1):
        counts.update(expand(template[idx:idx+2], steps))
    counts.update(template[-1])  # add last char in template manually

    freq = counts.most_common()
    return freq[0][1] - freq[-1][1]

def part1(template, rules):
    return polymerize(template, rules, 10)

def part2(template, rules):
    return polymerize(template, rules, 40)

def parse_input(data_src):
    data_src.seek(0)
    template = next(data_src).strip()
    next(data_src)
    rules = {}
    for line in data_src:
        a, b = line.strip().split(' -> ')
        rules[a] = b
    return template, rules

def run_tests():
    TEST_INPUT = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(*parse_input(test_data)) == 1588
    assert part2(*parse_input(test_data)) == 2188189693529

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, *parse_input(infile))  # 4244
        print_result('2', part2, *parse_input(infile))  # 4807056953866
