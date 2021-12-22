#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
from dataclasses import dataclass
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

@dataclass(frozen=True)
class Player:
    pos: int = 0
    score: int = 0
    turns: int = 0

def part1(p1_pos, p2_pos):
    p1, p2 = Player(pos=p1_pos), Player(pos=p2_pos)
    die = itertools.cycle(range(1, 101))

    while True:
        roll_total = sum(itertools.islice(die, 3))
        new_pos = (p1.pos+roll_total-1) % 10 + 1
        p1 = Player(new_pos, p1.score+new_pos, p1.turns+1)
        if p1.score >= 1000:
            break
        p1, p2 = p2, p1

    return p2.score * (p1.turns+p2.turns)*3

ROLLS = Counter(sum(roll) for roll in itertools.product(range(1, 4), repeat=3))

@functools.lru_cache(maxsize=None)
def count_wins(p1, p2):
    wins = np.zeros(2, dtype=int)
    for roll_total, freq in ROLLS.items():
        new_pos = (p1.pos+roll_total-1) % 10 + 1
        new_score = p1.score - new_pos
        if new_score <= 0:
            wins[0] += freq
        else:
            wins += freq * count_wins(p2, Player(new_pos, new_score))[::-1]
    return wins

def part2(p1_pos, p2_pos):
    return max(count_wins(Player(p1_pos, 21), Player(p2_pos, 21)))

def parse_input(data_src):
    data_src.seek(0)
    p1_pos = int(next(data_src).split()[-1])
    p2_pos = int(next(data_src).split()[-1])
    return p1_pos, p2_pos

def run_tests():
    TEST_INPUT = """
Player 1 starting position: 4
Player 2 starting position: 8
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(*parse_input(test_data)) == 739785
    assert part2(*parse_input(test_data)) == 444356092776315

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, *parse_input(infile))  # 513936
        print_result('2', part2, *parse_input(infile))  # 105619718613031
