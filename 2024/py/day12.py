#!/usr/bin/env python3
import time
import typing
from io import StringIO


def flood_fill(row, col, grid):
    ROWS = len(grid)
    COLS = len(grid[0])
    REGION_ID = grid[row][col]

    area = set()
    edges = []

    coords = [(row, col)]
    while coords:
        r, c = coords.pop()

        if (r, c) in area:
            continue

        if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == REGION_ID:
            area.add((r, c))

            for coord in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
                coords.append(coord)
        else:
            edges.append((r, c))

    return area, edges

def find_regions(grid):
    COLS = len(grid[0])

    flooded = set()
    regions = []
    for r, row in enumerate(grid):
        for c in range(COLS):
            if (r, c) in flooded:
                continue

            area, edges = flood_fill(r, c, grid)
            regions.append((area, edges))
            flooded |= area

    return regions

def part1(grid):
    return sum(len(area)*len(edges) for area, edges in find_regions(grid))

def part2(grid):
    ADJACENCY_VECTORS = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    cost = 0
    for area, edges in find_regions(grid):
        corners = 0  # num sides == num corners

        # count outer corners
        # NB: an area coord may represent 1, 2, or 4 outer corners
        for r, c in area:
            # if (two adjacent neighbors are edges) and
            #    (the cell between those edges isn't part of this region)
            # then this is an outer corner
            for adj_r, adj_c in ADJACENCY_VECTORS:
                if (
                    (r+adj_r, c) in edges and
                    (r, c+adj_c) in edges and
                    (r+adj_r, c+adj_c) not in area
                ):
                    corners += 1

        # count inner corners
        # NB: each inner corner appears multiple times in edges; don't overcount
        for r, c in set(edges):
            # if (two adjacent neighbors are in the region)
            # then this is an inner corner
            for adj_r, adj_c in ADJACENCY_VECTORS:
                if (
                    (r+adj_r, c) in area and
                    (r, c+adj_c) in area
                ):
                    corners += 1

        cost += len(area) * corners

    return cost

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read().splitlines()]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 1319878

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 784982

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
    TEST_ANSWER1 = 1930

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 1206

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
