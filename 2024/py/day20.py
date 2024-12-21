#!/usr/bin/env python3
import itertools
import time
import typing
from io import StringIO


def measure_track(grid, start, end):
    r, c = end
    dists = dict()
    for picos in itertools.count():
        dists[r, c] = picos

        if (r, c) == start:
            break

        for step in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if step not in dists and grid[step[0]][step[1]] != "#":
                r, c = step
                break

    return dists


# iterate over region a max manhattan distance from center
def manhattan_region(max_dist):
    for r in range(-max_dist, max_dist+1):
        c_limit = max_dist - abs(r)
        for c in range(-c_limit, c_limit+1):
            yield r, c


def count_savings(grid, start, end, max_cheat, min_savings=100):
    dists = measure_track(grid, start, end)

    count = 0
    for offset in manhattan_region(max_cheat):  # invert loops for fasterness
        for a in dists:
            b = a[0]+offset[0], a[1]+offset[1]
            cheat_len = abs(offset[0]) + abs(offset[1])
            if b in dists and dists[a] - dists[b] - cheat_len >= min_savings:
                count += 1
    return count


def part1(grid, start, end):
    return count_savings(grid, start, end, 2)


def part2(grid, start, end):
    return count_savings(grid, start, end, 20)


def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    grid = []
    for r, row in enumerate(data_src.read().splitlines()):
        grid.append(row)
        if (c := row.find("S")) != -1:
            start = r, c
        if (c := row.find("E")) != -1:
            end = r, c
    return [grid, start, end]


def main():
    with open(__file__[:-3] + "-input.dat") as infile:
        solve_part("1", part1, *parse_input(infile))  # 1530
        solve_part("2", part2, *parse_input(infile))  # 1033983


def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")


def get_test_data() -> tuple[tuple[str, str | float], tuple[str, str | float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
    TEST_ANSWER1 = float("nan")

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float("nan")

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2),
    )


if __name__ == "__main__":
    main()
