#!/usr/bin/env python3
import functools
import operator
import time
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(cubes):
    surface = 0
    for x, y, z in cubes:
        if (x-1, y, z) not in cubes:
            surface += 1
        if (x+1, y, z) not in cubes:
            surface += 1
        if (x, y-1, z) not in cubes:
            surface += 1
        if (x, y+1, z) not in cubes:
            surface += 1
        if (x, y, z-1) not in cubes:
            surface += 1
        if (x, y, z+1) not in cubes:
            surface += 1
    return surface

def part2(cubes):
    x_bounds = (min(cubes, key=operator.itemgetter(0)),
                max(cubes, key=operator.itemgetter(0)))
    y_bounds = (min(cubes, key=operator.itemgetter(1)),
                max(cubes, key=operator.itemgetter(1)))
    z_bounds = (min(cubes, key=operator.itemgetter(2)),
                max(cubes, key=operator.itemgetter(2)))

    @functools.lru_cache(maxsize=None)
    def exposed(x, y, z):
        """flood fill and check if it ever leaks past boundary"""
        checked = set(cubes)
        fill = [(x, y, z)]
        while fill:
            x, y, z = fill.pop()
            if (x, y, z) in checked:
                continue

            if (x < x_bounds[0][0] or x > x_bounds[1][0] or
                y < y_bounds[0][1] or y > y_bounds[1][1] or
                z < z_bounds[0][2] or z > z_bounds[1][2]
            ):
                return True

            checked.add((x, y, z))
            fill.append((x-1, y, z))
            fill.append((x+1, y, z))
            fill.append((x, y-1, z))
            fill.append((x, y+1, z))
            fill.append((x, y, z-1))
            fill.append((x, y, z+1))
        return False

    surface = 0
    for x, y, z in tqdm(cubes):
        if exposed(x-1, y, z):
            surface += 1
        if exposed(x+1, y, z):
            surface += 1
        if exposed(x, y-1, z):
            surface += 1
        if exposed(x, y+1, z):
            surface += 1
        if exposed(x, y, z-1):
            surface += 1
        if exposed(x, y, z+1):
            surface += 1
    return surface

def parse_input(data_src):
    data_src.seek(0)
    cubes = set()
    for line in data_src.read().splitlines():
        cubes.add(tuple(map(int, line.split(','))))
    return [cubes]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 3542

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 2080

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (64, 58)
    TEST_INPUT = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
