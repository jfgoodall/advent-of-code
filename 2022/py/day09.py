#!/usr/bin/env python3
import time
from io import StringIO


def sign(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0

def move_head(direction, head):
    assert direction in 'RLUD'
    if direction == 'R': head[0] += 1
    elif direction == 'L': head[0] -= 1
    elif direction == 'U': head[1] += 1
    else : head[1] -= 1  # 'D'

def move_tail(head, tail):
    if abs(head[0]-tail[0]) > 1 or abs(head[1]-tail[1]) > 1:
        tail[0] += sign(head[0]-tail[0])
        tail[1] += sign(head[1]-tail[1])

def part1(instr):
    head = [0, 0]
    tail = [0, 0]
    visited = {tuple(tail)}

    for direction, count in instr:
        for _ in range(count):
            move_head(direction, head)
            move_tail(head, tail)
            visited.add(tuple(tail))
    return len(visited)

def part2(instr):
    knots = [[0, 0] for _ in range(10)]
    visited = {tuple(knots[-1])}

    for direction, count in instr:
        for _ in range(count):
            move_head(direction, knots[0])
            for idx in range(1, len(knots)):
                move_tail(knots[idx-1], knots[idx])
            visited.add(tuple(knots[-1]))
    return len(visited)

def parse_input(data_src):
    data_src.seek(0)
    instr = []
    for line in data_src:
        a, b = line.strip().split()
        instr.append((a, int(b)))
    return instr

def run_tests():
    TEST_INPUT = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 13
    assert part2(parse_input(test_data)) == 1

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 6212
        print_result('2', part2, parse_input(infile))  # 2522
