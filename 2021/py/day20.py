#!/usr/bin/env python3
import time
from io import StringIO

import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def dump_image(image):
    for row in image:
        print(''.join('#' if c else '.' for c in row))

def enhance(algo, image, passes):
    assert passes % 2 == 0
    assert algo[0] == 0 or algo[-1] == 0

    for p in tqdm(range(passes), ncols=80, leave=False):
        infinite_pts = 1 if algo[0] and p%2==1 else 0
        image = np.pad(image, 2, constant_values=infinite_pts)
        enhanced = np.empty((image.shape[0]-2, image.shape[1]-2), dtype=int)
        for row in range(image.shape[0]-2):
            for col in range(image.shape[1]-2):
                bits = image[row:row+3, col:col+3].reshape(9)
                idx = int(''.join(str(bit) for bit in bits), 2)
                enhanced[row, col] = algo[idx]
        image = enhanced
    return image.sum()

def part1(algo, image):
    return enhance(algo, image, 2)

def part2(algo, image):
    return enhance(algo, image, 50)

def parse_input(data_src):
    data_src.seek(0)
    algo_str = next(data_src).strip()
    algo = np.where(np.array(list(algo_str))=='.', 0, 1)
    next(data_src)

    image_str = data_src.readlines()
    image = np.empty((len(image_str), len(image_str[0].strip())), dtype=int)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            image[row,col] = 0 if image_str[row][col]=='.' else 1

    return algo, image

def run_tests():
    TEST_INPUT = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

...............
...............
...............
...............
...............
.....#..#......
.....#.........
.....##..#.....
.......#.......
.......###.....
...............
...............
...............
...............
...............
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(*parse_input(test_data)) == 35
    assert part2(*parse_input(test_data)) == 3351

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, *parse_input(infile))  # -
        print_result('2', part2, *parse_input(infile))  # -
