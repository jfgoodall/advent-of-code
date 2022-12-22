#!/usr/bin/env python3
import re
import time
from io import StringIO


def dump(grid):
    for row in grid:
        print('-', ''.join(row), '-')

def walk_up(grid, steps, row, col, bounds):
    for _ in range(steps):
        next_pos = bounds[1]-1 if row-1 < bounds[0] else row-1
        if grid[next_pos][col] == '#':
            break
        row = next_pos
    return row, col

def walk_right(grid, steps, row, col, bounds):
    for _ in range(steps):
        next_pos = bounds[0] if col+1 == bounds[1] else col+1
        if grid[row][next_pos] == '#':
            break
        col = next_pos
    return row, col

def walk_down(grid, steps, row, col, bounds):
    for _ in range(steps):
        next_pos = bounds[0] if row+1 == bounds[1] else row+1
        if grid[next_pos][col] == '#':
            break
        row = next_pos
    return row, col

def walk_left(grid, steps, row, col, bounds):
    for _ in range(steps):
        next_pos = bounds[1]-1 if col-1 < bounds[0] else col-1
        if grid[row][next_pos] == '#':
            break
        col = next_pos
    return row, col

def part1(grid, path):
    # determine in-bounds for each row & col
    row_bounds = []
    for row in grid:
        for start, ch in enumerate(row):
            if ch != ' ':
                break
        end = start
        while end < len(row) and row[end] != ' ':
            end += 1
        row_bounds.append((start, end))

    col_bounds = []
    for col in range(len(grid[0])):
        for start, row in enumerate(grid):
            if row[col] != ' ':
                break
        end = start
        while end < len(grid) and grid[end][col] != ' ':
            end += 1
        col_bounds.append((start, end))

    row = 0
    for col, ch in enumerate(grid[0]):
        if ch == '.':
            break
    facing = 'U'  # first turn is always 'R'

    for turn, steps in path:
        if turn == 'R':
            if facing == 'U': facing = 'R'
            elif facing == 'R': facing = 'D'
            elif facing == 'D': facing = 'L'
            elif facing == 'L': facing = 'U'
            else: assert False
        elif turn == 'L':
            if facing == 'U': facing = 'L'
            elif facing == 'L': facing = 'D'
            elif facing == 'D': facing = 'R'
            elif facing == 'R': facing = 'U'
            else: assert False
        else:
            assert False

        if facing == 'U':
            row, col = walk_up(grid, steps, row, col, col_bounds[col])
        elif facing == 'R':
            row, col = walk_right(grid, steps, row, col, row_bounds[row])
        elif facing == 'D':
            row, col = walk_down(grid, steps, row, col, col_bounds[col])
        else:
            row, col = walk_left(grid, steps, row, col, row_bounds[row])

    return 1000*(row+1) + 4*(col+1) + {'R':0, 'D':1, 'L':2, 'U':3}[facing]

def cube_up(grid, steps, row, col):
    facing = 'U'
    for stepped in range(steps):
        if col < 50 and row-1 < 100:
            new_row = 50 + col
            new_col = 50
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_right(grid, steps-stepped-1, new_row, new_col)
        elif col >= 50 and col < 100 and row-1 < 0:
            new_row = 150 + col - 50
            new_col = 0
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_right(grid, steps-stepped-1, new_row, new_col)
        elif col >= 100 and row-1 < 0:
            new_row = 199
            new_col = col - 100
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_up(grid, steps-stepped-1, new_row, new_col)
        else:
            new_row = row-1
            if grid[new_row][col] == '#':
                break
            row = new_row
    return row, col, facing

def cube_right(grid, steps, row, col):
    facing = 'R'
    for stepped in range(steps):
        if row < 50 and col+1 == 150:
            new_row = (50-row-1) + 100
            new_col = 99
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_left(grid, steps-stepped-1, new_row, new_col)
        elif row >= 50 and row < 100 and col+1 == 100:
            new_row = 49
            new_col = 100 + row - 50
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_up(grid, steps-stepped-1, new_row, new_col)
        elif row >= 100 and row < 150 and col+1 == 100:
            new_row = (150-row-1)
            new_col = 149
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_left(grid, steps-stepped-1, new_row, new_col)
        elif row >= 150 and col+1 == 50:
            new_row = 149
            new_col = 50 + row - 150
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_up(grid, steps-stepped-1, new_row, new_col)
        else:
            new_col = col+1
            if grid[row][new_col] == '#':
                break
            col = new_col
    return row, col, facing

def cube_down(grid, steps, row, col):
    facing = 'D'
    for stepped in range(steps):
        if col < 50 and row+1 == 200:
            new_row = 0
            new_col = col + 100
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_down(grid, steps-stepped-1, new_row, new_col)
        elif col >= 50 and col < 100 and row+1 == 150:
            new_row = 150 + col - 50
            new_col = 49
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_left(grid, steps-stepped-1, new_row, new_col)
        elif col >= 100 and row+1 == 50:
            new_row = 50 + col - 100
            new_col = 99
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_left(grid, steps-stepped-1, new_row, new_col)
        else:
            new_row = row+1
            if grid[new_row][col] == '#':
                break
            row = new_row
    return row, col, facing

def cube_left(grid, steps, row, col):
    facing = 'L'
    for stepped in range(steps):
        if row < 50 and col-1 < 50:
            new_row = (50-row-1) + 100
            new_col = 0
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_right(grid, steps-stepped-1, new_row, new_col)
        elif row >= 50 and row < 100 and col-1 < 50:
            new_row = 100
            new_col = row - 50
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_down(grid, steps-stepped-1, new_row, new_col)
        elif row >= 100 and row < 150 and col-1 < 0:
            new_row = (150-row-1)
            new_col = 50
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_right(grid, steps-stepped-1, new_row, new_col)
        elif row >= 150 and col-1 < 0:
            new_row = 0
            new_col = 50 + row - 150
            if grid[new_row][new_col] == '#':
                return row, col, facing
            return cube_down(grid, steps-stepped-1, new_row, new_col)
        else:
            new_col = col-1
            if grid[row][new_col] == '#':
                break
            col = new_col
    return row, col, facing

def part2(grid, path):
    row = 0
    for col, ch in enumerate(grid[0]):
        if ch == '.':
            break
    facing = 'U'  # first turn is always 'R'

    for turn, steps in path:
        if turn == 'R':
            if facing == 'U': facing = 'R'
            elif facing == 'R': facing = 'D'
            elif facing == 'D': facing = 'L'
            elif facing == 'L': facing = 'U'
            else: assert False
        elif turn == 'L':
            if facing == 'U': facing = 'L'
            elif facing == 'L': facing = 'D'
            elif facing == 'D': facing = 'R'
            elif facing == 'R': facing = 'U'
            else: assert False
        else:
            assert False

        if facing == 'U':
            row, col, facing = cube_up(grid, steps, row, col)
        elif facing == 'R':
            row, col, facing = cube_right(grid, steps, row, col)
        elif facing == 'D':
            row, col, facing = cube_down(grid, steps, row, col)
        else:
            row, col, facing = cube_left(grid, steps, row, col)

    return 1000*(row+1) + 4*(col+1) + {'R':0, 'D':1, 'L':2, 'U':3}[facing]

def parse_input(data_src):
    data_src.seek(0)

    grid_chars, path_chars = data_src.read().split('\n\n')
    grid_chars = grid_chars.splitlines()

    width = max(len(row) for row in grid_chars)
    grid = []
    for row in grid_chars:
        grid.append(list(row) + [' ' for _ in range(width-len(row))])

    PATH_RE = re.compile(r'([LR])(\d+)')
    # add a right turn to the front to keep data as (turn, steps) pairs
    path = [(x, int(y)) for x, y in PATH_RE.findall('R'+path_chars)]

    return [grid, path]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 65368

        # skip test because the datasets have different cube face layouts
        # assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 156166

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (6032, 5031)
    TEST_INPUT = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5\
"""
    return StringIO(TEST_INPUT), TEST_RESULTS

if __name__ == '__main__':
    main()
