#!/usr/bin/env python3
from io import StringIO
import numpy as np
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable
from collections import Counter
import itertools

DIGIT_MAP = {
        'abcefg': 0,
        'cf': 1,
        'acdeg': 2,
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9
    }
DIGIT_SET = set(DIGIT_MAP.keys())

def part1(lines):
    counts = Counter()
    for line in lines:
        counts.update(len(val) for val in line[1])
    return sum(counts[x] for x in (2, 3, 4, 7))

def translate(s, table):
    return ''.join(sorted(table[ch] for ch in s))

def part2(lines):
    output_sum = 0
    for line in tqdm(lines):
        # brute forcing 7! possible translations
        for perm in itertools.permutations('abcdefg'):
            table = {'abcdefg'[i]: perm[i] for i in range(len(perm))}
            xlated = {translate(digit, table) for digit in line[0]}
            if xlated == DIGIT_SET:
                break
        else:
            assert False

        value = 0
        xlated = [translate(digit, table) for digit in line[1]]
        for digit in xlated:
            value = value * 10 + DIGIT_MAP[digit]
        output_sum += value
    return output_sum

def parse_input(data_src):
    inp = data_src.readlines()

    def sort_strings(s):
        return [''.join(sorted(x)) for x in s]

    parsed = []
    for line in inp:
        line = line.split()
        parsed.append((sort_strings(line[:10]), sort_strings(line[-4:])))
    return parsed

def run_tests():
    TEST_INPUT = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 26
    assert part2(parsed) == 61229

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 367
    print(f"Part 2: {part2(parsed)}")  # 974512
