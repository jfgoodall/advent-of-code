#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np


def part1(trees):
    visible = sum(trees.shape*2) - 4  # perimeter trees
    for i in range(1, trees.shape[0]-1):
        for j in range(1, trees.shape[1]-1):
            if (np.all(trees[i,j] > trees[i,:j]) or    # left
                np.all(trees[i,j] > trees[i,j+1:]) or  # right
                np.all(trees[i,j] > trees[:i,j]) or    # up
                np.all(trees[i,j] > trees[i+1:,j])     # down
            ):
                visible += 1
    return visible

def part2(trees):
    best_score = 0
    for i in range(1, trees.shape[0]-1):
        for j in range(1, trees.shape[1]-1):
            for left, height in enumerate(np.flip(trees[i,:j]), 1):
                if height >= trees[i,j]: break
            for right, height in enumerate(trees[i,j+1:], 1):
                if height >= trees[i,j]: break
            for up, height in enumerate(np.flip(trees[:i,j]), 1):
                if height >= trees[i,j]: break
            for down, height in enumerate(trees[i+1:,j], 1):
                if height >= trees[i,j]: break
            best_score = max(best_score, left*right*up*down)

            # this way is a faster, but feels less pythonic
            #
            # left = i - 1
            # while left > 0 and trees[i,j] > trees[left,j]:
            #     left -= 1
            # right = i + 1
            # while right < trees.shape[0]-1 and trees[i,j] > trees[right,j]:
            #     right += 1
            # up = j - 1
            # while up > 0 and trees[i,j] > trees[i,up]:
            #     up -= 1
            # down = j + 1
            # while down < trees.shape[1]-1 and trees[i,j] > trees[i,down]:
            #     down += 1
            # score = (i-left) * (right-i) * (j-up) * (down-j)
            # best_score = max(best_score, score)

    return best_score


def parse_input(data_src):
    data_src.seek(0)
    trees = [[int(x) for x in line.strip()] for line in data_src]
    return np.array(trees)

def run_tests():
    TEST_INPUT = """
30373
25512
65332
33549
35390
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 21
    assert part2(parse_input(test_data)) == 8

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 1676
        print_result('2', part2, parse_input(infile))  # 313200
