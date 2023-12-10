#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

def find_loop(grid):
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == 'S':
                break
        else:
            continue
        break
    pos = np.array((i, j))

    directions = []
    if pos[1] > 0 and grid[pos[0]][pos[1]-1] in '-FL':
        directions.append(LEFT)  # go left
    if pos[1] < len(grid[0])-1 and grid[pos[0]][pos[1]+1] in '-J7':
        directions.append(RIGHT)  # go right
    if pos[0] > 0 and grid[pos[0]-1][pos[1]] in '|F7':
        directions.append(UP)  # go up
    if pos[0] < len(grid)-1 and grid[pos[0]+1][pos[1]] in '|LJ':
        directions.append(DOWN)  # go down

    directions.sort()
    if directions == sorted([UP, RIGHT]):
        S = 'L'
    elif directions == sorted([UP, LEFT]):
        S = 'J'
    elif directions == sorted([UP, DOWN]):
        S = '|'
    elif directions == sorted([DOWN, RIGHT]):
        S = 'F'
    elif directions == sorted([DOWN, LEFT]):
        S = '7'
    elif directions == sorted([LEFT, RIGHT]):
        S = '-'
    start_pos = np.array((i, j))

    direction = directions[0]
    loop_pts = set()
    while True:
        pos += direction
        match grid[pos[0]][pos[1]]:
            case 'F':
                if direction == UP:
                    direction = RIGHT
                elif direction == LEFT:
                    direction = DOWN
            case 'J':
                if direction == DOWN:
                    direction = LEFT
                elif direction == RIGHT:
                    direction = UP
            case '7':
                if direction == UP:
                    direction = LEFT
                elif direction == RIGHT:
                    direction = DOWN
            case 'L':
                if direction == DOWN:
                    direction = RIGHT
                elif direction == LEFT:
                    direction = UP
        loop_pts.add(tuple(pos))
        if grid[pos[0]][pos[1]] == 'S':
            break

    # change 'S' to the correct symbol
    grid[start_pos[0]][start_pos[1]] = S

    return loop_pts

def part1(grid):
    loop_pts = find_loop(grid)
    return len(loop_pts) // 2

def part2(grid):
    loop_pts = find_loop(grid)

    # overwrite junk pipes with '.'
    for row, col in np.ndindex((len(grid), len(grid[0]))):
        if (row, col) not in loop_pts:
            grid[row][col] = '.'

    # count the number of points within the polygon defined by the loop by
    # scanning across the rows and counting the edges crossed
    area = 0
    for row in range(len(grid)):
        edges = 0
        for col in range(len(grid[0])):
            match c := grid[row][col]:
                case '.':
                    area += edges % 2
                case '|':
                    edges += 1
                case 'F' | 'L':
                    corner = c
                case 'J' | '7':
                    if (corner, c) in (('L', '7'), ('F', 'J')):
                        edges += 1
    return area

def parse_input(data_src):
    data_src.seek(0)
    lines = [list(line) for line in data_src.read().splitlines()]
    return [lines]

def main():
    with open(__file__[:-3] + '-input.dat') as infile:
        test_data, test_answers = get_test_data1()
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 6701

        test_data, test_answers = get_test_data2()
        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 303

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data1():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (8, 0)
    TEST_INPUT = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

def get_test_data2():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (0, 4)
    TEST_INPUT = """
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
