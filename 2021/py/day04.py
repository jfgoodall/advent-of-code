#!/usr/bin/env python3
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def play_number(boards, number):
    boards[:,:,1] += boards[:,:,0] == number

def check_boards(boards):
    winners = []
    for idx, board in enumerate(boards):
        square = board.reshape(5, 5, 2)
        for i in range(5):
            if square[i,:,1].all() or square[:,i,1].all():
                winners.append(idx)
    return winners

def part1(numbers, boards):
    for num in numbers:
        play_number(boards, num)
        if winners := check_boards(boards):
            assert len(winners) == 1
            winner = boards[winners[0]]
            return num * winner[winner[:,1]==0].sum()

def part2(numbers, boards):
    for num in numbers:
        play_number(boards, num)
        winners = check_boards(boards)
        if winners and len(boards) == 1:
            return num * boards[boards[:,:,1]==0].sum()
        boards = np.delete(boards, winners, axis=0)

def parse_input(data_src):
    numbers = list(map(int, data_src.readline().split(',')))

    lines = data_src.readlines()
    boards = []
    idx = 0
    while idx < len(lines):
        idx += 1  # blank line
        board = []
        for _ in range(5):
            board.extend([int(c), 0] for c in lines[idx].split())
            idx += 1
        boards.append(board)
    return numbers, np.asarray(boards)

def run_tests():
    TEST_INPUT = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
    with StringIO(TEST_INPUT.strip()) as test_data:
        numbers, boards = parse_input(test_data)
    assert part1(numbers, boards.copy()) == 4512
    assert part2(numbers, boards.copy()) == 1924

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        numbers, boards = parse_input(infile)
    print(f"Part 1: {part1(numbers, boards.copy())}")  # 74320
    print(f"Part 2: {part2(numbers, boards.copy())}")  # 17884
