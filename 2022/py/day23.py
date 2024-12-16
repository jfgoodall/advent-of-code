#!/usr/bin/env python3
import itertools
import time
from collections import defaultdict
from io import StringIO


def bounding_box(elves):
    elf_iter = iter(elves)
    x, y = next(elf_iter)
    min_x, min_y = x, y
    max_x, max_y = x, y
    for x, y in elf_iter:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return width, height, min_x, min_y

def dump(elves):
    width, height, x_offset, y_offset = bounding_box(elves)
    grid = [list('.'*width) for _ in range(height)]
    for x, y in elves:
        grid[y-y_offset][x-x_offset] = '#'
    for row in reversed(grid):
        print(''.join(row))

def move_elves(elves, directions):
    proposed = defaultdict(list)  # { dest_coord: [source_coords] }
    for x, y in elves:
        NE = (x+1, y+1) in elves
        N  = (x  , y+1) in elves
        NW = (x-1, y+1) in elves
        E  = (x+1, y  ) in elves
        W  = (x-1, y  ) in elves
        SE = (x+1, y-1) in elves
        S  = (x  , y-1) in elves
        SW = (x-1, y-1) in elves
        if not (NE or N or NW or W or E or SE or S or SW):
            continue

        for direction in directions:
            if direction == 'N' and not (NE or N or NW):
                proposed[(x, y+1)].append((x, y))
                break
            elif direction == 'S' and not (SE or S or SW):
                proposed[(x, y-1)].append((x, y))
                break
            elif direction == 'W' and not (NW or W or SW):
                proposed[(x-1, y)].append((x, y))
                break
            elif direction == 'E' and not (NE or E or SE):
                proposed[(x+1, y)].append((x, y))
                break

    for dest, src in proposed.items():
        if len(src) == 1:
            elves.remove(src[0])
            elves.add(dest)

    return len(proposed) > 0

def part1(elves):
    dir_prio = itertools.cycle('NSWE')
    for _ in range(10):
        move_elves(elves, list(itertools.islice(dir_prio, 4)))
        next(dir_prio)

    width, height, *_ = bounding_box(elves)
    return width * height - len(elves)

def part2(elves):
    dir_prio = itertools.cycle('NSWE')
    for rnd in itertools.count(1):
        if not move_elves(elves, list(itertools.islice(dir_prio, 4))):
            return rnd
        next(dir_prio)

def parse_input(data_src):
    data_src.seek(0)
    elves = set()
    for y, line in enumerate(reversed(data_src.read().splitlines())):
        for x, ch in enumerate(line):
            if ch == '#':
                elves.add((x, y))
    return [elves]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 3815

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 893

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (110, 20)
    TEST_INPUT = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
