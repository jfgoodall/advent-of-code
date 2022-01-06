#!/usr/bin/env python3
import functools
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

BRACKETS = {'(': ')', '[': ']', '{': '}', '<': '>'}

def part1(lines):
    SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
    total_score = 0
    for line in lines:
        brackets = []
        for ch in line:
            try:
                brackets.append(BRACKETS[ch])
            except KeyError:
                if ch != brackets.pop():
                    total_score += SCORE[ch]
                    break
    return total_score

def part2(lines):
    SCORE = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for line in lines:
        brackets = []
        for ch in line:
            try:
                brackets.append(BRACKETS[ch])
            except KeyError:
                if ch != brackets.pop():
                    break
        else:
            scores.append(functools.reduce(lambda a, b: a*5+b,
                                           map(SCORE.get, reversed(brackets))))
    return int(np.median(scores))

def parse_input(data_src):
    return [line.strip() for line in data_src]

def run_tests():
    TEST_INPUT = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        parsed = parse_input(test_data)
    assert part1(parsed) == 26397
    assert part2(parsed) == 288957

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        parsed = parse_input(infile)
    print(f"Part 1: {part1(parsed)}")  # 311949
    print(f"Part 2: {part2(parsed)}")  # 3042730309
