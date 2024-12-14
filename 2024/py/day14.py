#!/usr/bin/env python3
import time
import typing

import numpy as np
from scipy.spatial.distance import pdist

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable


def part1(robots):
    WIDTH = 101
    HEIGHT = 103

    q1, q2, q3, q4 = 0, 0, 0, 0
    for (x, y), (dx, dy) in robots:
        x = (x + dx * 100) % WIDTH
        y = (y + dy * 100) % HEIGHT
        if x < WIDTH // 2 and y < HEIGHT // 2:
            q1 += 1
        elif x > WIDTH // 2 and y < HEIGHT // 2:
            q2 += 1
        elif x < WIDTH // 2 and y > HEIGHT // 2:
            q3 += 1
        elif x > WIDTH // 2 and y > HEIGHT // 2:
            q4 += 1

    return q1 * q2 * q3 * q4

def part2(robots):
    WIDTH = 101
    HEIGHT = 103

    pos = np.array([[x, y] for (x, y), _ in robots])
    vel = np.array([[dx, dy] for _, (dx, dy) in robots])
    bounds = np.array((WIDTH, HEIGHT))

    # find minimum average distance between all pairwise points
    min_pd = float('inf'), 0
    for seconds in tqdm(range(WIDTH*HEIGHT)):
        updated = (pos + vel*seconds) % bounds
        min_pd = min(min_pd, (np.mean(pdist(updated)), seconds))

    tree_sec = min_pd[1]

    # render the positions of the robots at the time found
    grid = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for idx, ((x, y), (dx, dy)) in enumerate(robots):
        x = (x + dx * tree_sec) % WIDTH
        y = (y + dy * tree_sec) % HEIGHT
        grid[y][x] = '@'
    print('\n'.join(''.join(line) for line in grid))

    return tree_sec

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    robots = []
    for line in data_src.read().splitlines():
        p, v = line.split()
        p = tuple(map(int, p[2:].split(',')))
        v = tuple(map(int, v[2:].split(',')))
        robots.append((p, v))
    return [robots]

def main():
    with open(__file__[:-3] + '-input.dat') as infile:
        solve_part('1', part1, *parse_input(infile))  # 230172768
        solve_part('2', part2, *parse_input(infile))  # 8087

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    main()
