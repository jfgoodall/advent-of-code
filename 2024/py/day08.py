#!/usr/bin/env python3
import itertools
import time
import typing
from collections import defaultdict
from io import StringIO


def part1(antennas, height, width):
    antinodes = set()
    for locs in antennas.values():
        for a1, a2 in itertools.combinations(locs, 2):
            d = a1[0]-a2[0], a1[1]-a2[1]

            anti = a1[0]+d[0], a1[1]+d[1]
            if 0 <= anti[0] < height and 0 <= anti[1] < width:
                antinodes.add(anti)

            anti = a2[0]-d[0], a2[1]-d[1]
            if 0 <= anti[0] < height and 0 <= anti[1] < width:
                antinodes.add(anti)

    return len(antinodes)

def part2(antennas, height, width):
    antinodes = set()
    for locs in antennas.values():
        for a1, a2 in itertools.combinations(locs, 2):
            d = a1[0]-a2[0], a1[1]-a2[1]

            anti = a1
            while 0 <= anti[0] < height and 0 <= anti[1] < width:
                antinodes.add(anti)
                anti = anti[0]+d[0], anti[1]+d[1]

            anti = a2
            while 0 <= anti[0] < height and 0 <= anti[1] < width:
                antinodes.add(anti)
                anti = anti[0]-d[0], anti[1]-d[1]

    return len(antinodes)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    grid = data_src.read().splitlines()
    antennas = defaultdict(set)
    for row, line in enumerate(grid):
        for col, ch in enumerate(line):
            if ch != '.':
                antennas[ch].add((row, col))
    return [antennas, len(grid), len(grid[0])]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # -

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # -

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
    TEST_ANSWER1 = 14

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 34

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
