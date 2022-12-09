#!/usr/bin/env python3
import time
from enum import Enum
from io import StringIO


class Shape(Enum):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

PTS_FOR_SHAPE = { Shape.ROCK: 1,
                  Shape.PAPER: 2,
                  Shape.SCISSORS: 3 }

SHAPE_MAP = { 'A': Shape.ROCK, 'X': Shape.ROCK,
              'B': Shape.PAPER, 'Y': Shape.PAPER,
              'C': Shape.SCISSORS, 'Z': Shape.SCISSORS }


def points_for_round(theirs, mine):
    if theirs == mine:
        return 3
    if (theirs == Shape.ROCK and mine == Shape.PAPER or
        theirs == Shape.SCISSORS and mine == Shape.ROCK or
        theirs == Shape.PAPER and mine == Shape.SCISSORS
    ):
        return 6
    return 0

def part1(rounds):
    points = 0
    for abc, xyz in rounds:
        theirs = SHAPE_MAP[abc]
        mine = SHAPE_MAP[xyz]
        points += PTS_FOR_SHAPE[mine] + points_for_round(theirs, mine)
    return points

def part2(rounds):
    points = 0
    for abc, xyz in rounds:
        theirs = SHAPE_MAP[abc]
        if xyz == 'X':  # force a loss
            if theirs == Shape.ROCK: mine = Shape.SCISSORS
            elif theirs == Shape.PAPER: mine = Shape.ROCK
            else: mine = Shape.PAPER
        elif xyz == 'Y':  # force a tie
            mine = theirs
        else:  # force a win
            if theirs == Shape.ROCK: mine = Shape.PAPER
            elif theirs == Shape.PAPER: mine = Shape.SCISSORS
            else: mine = Shape.ROCK
        points += PTS_FOR_SHAPE[mine] + points_for_round(theirs, mine)
    return points

def parse_input(data_src):
    data_src.seek(0)
    return [line.strip().split() for line in data_src]

def run_tests():
    TEST_INPUT = """
A Y
B X
C Z
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 15
    assert part2(parse_input(test_data)) == 12

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 9177
        print_result('2', part2, parse_input(infile))  # 12111
