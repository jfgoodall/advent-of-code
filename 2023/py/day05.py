#!/usr/bin/env python3
import itertools
import time
from collections import defaultdict
from io import StringIO


def part1(seeds, mapping, mapped_vals, _):
    location = float('inf')
    for seed in seeds:
        current_src = 'seed'
        while True:
            for dest, src, count in mapped_vals[current_src]:
                if seed >= src and seed < src+count:
                    seed = dest+(seed-src)
                    break
            if current_src == 'location':
                break
            current_src = mapping[current_src]
        location = min(seed, location)
    return location

# this works...but took 3.5 minutes to run. i think an optimal solution might be some
# kind of tree structure to subdivide the ranges and narrow down the search space
def part2(seeds, _, mapped_vals, rev_mapping):
    # start from location zero and work backwards until we find a valid solution
    seed_starts = seeds[::2]
    seed_counts = seeds[1::2]
    seeds = sorted(list(zip(seed_starts, seed_counts)))

    for location in itertools.count():
        current_dest = 'location'
        seed = location
        while True:
            for dest, src, count in mapped_vals[current_dest]:
                if seed >= dest and seed < dest+count:
                    seed = src+(seed-dest)
                    break
            if current_dest == 'seed':
                break
            current_dest = rev_mapping[current_dest]

        # check if seed value fall within a valid starting range
        for start, count in seeds:
            if seed >= start and seed < start+count:
                return location

def parse_input(data_src):
    data_src.seek(0)
    seeds = list(map(int, data_src.readline().split(':')[1].split()))

    mapping = {}
    rev_mapping = {}
    mapped_vals = defaultdict(list)
    current_dest = None
    for line in data_src.read().splitlines():
        if not line:
            continue

        if not line[0].isnumeric():
            src, dest = line.split()[0].split('-to-')
            mapping[src] = dest
            rev_mapping[dest] = src
            current_dest = dest
        else:
            mapped_vals[src].append(tuple(map(int, line.split())))

    return [seeds, mapping, mapped_vals, rev_mapping]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 157211394

        assert part2(*parse_input(test_data)) == test_answers[1]
        # print_result('2', part2, *parse_input(infile))  # 50855035

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (35, 46)
    TEST_INPUT = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
