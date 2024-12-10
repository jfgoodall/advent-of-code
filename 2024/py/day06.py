#!/usr/bin/env python3
import time
import typing
from io import StringIO


def find_starting_location(grid):
    vec = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(list(row)):
            match cell:
                case '^':
                    vec = (-1, 0)
                case 'v':
                    vec = (1, 0)
                case '<':
                    vec = (0, -1)
                case '>':
                    vec = (0, 1)
                case _:
                    continue
            pos = (r, c)
            break
        if vec: break

    return pos, vec

def walk_patrol(grid, pos, vec, obstacle=None):
    ROWS = len(grid)
    COLS = len(grid[0])

    visited = {(pos, vec)}
    while True:
        next = pos[0]+vec[0], pos[1]+vec[1]
        if 0 <= next[0] < ROWS and 0 <= next[1] < COLS:
            if grid[next[0]][next[1]] == '#' or next == obstacle:
                vec = vec[1], -vec[0]  # turn right
            else:
                pos = next
                if (pos, vec) in visited:
                    return None  # patrol is a loop
                visited.add((pos, vec))
        else:
            break

    return {v[0] for v in visited}

def part1(grid):
    pos, vec = find_starting_location(grid)
    visited = walk_patrol(grid, pos, vec)
    return len(visited)

def part2(grid):
    pos, vec = find_starting_location(grid)
    obstacles = walk_patrol(grid, pos, vec)
    obstacles.remove(pos)

    loops = 0
    for obstacle in obstacles:
        visited = walk_patrol(grid, pos, vec, obstacle)
        if visited is None:
            loops += 1

    return loops

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read().splitlines()]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 5086

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 1770

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    TEST_ANSWER1 = 41

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 6

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
