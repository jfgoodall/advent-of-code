#!/usr/bin/env python3
import re
import time
from io import StringIO

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def part1(coords, y=2000000):
    nulls = []
    for sensor, beacon in coords:
        dist = manhattan(sensor, beacon)
        row_offset = abs(y-sensor[1])
        if row_offset < dist:
            half_width = dist - row_offset
            start = sensor[0] - half_width
            end = sensor[0] + half_width
            if beacon == (start, y):
                start += 1
            if beacon == (end, y):
                end -= 1
            nulls.append((start, end))

    # merge any overlapping ranges together
    nulls.sort(key=lambda pt: pt[0])
    combined = [nulls[0]]
    for null in nulls[1:]:
        if null[0] > combined[-1][1]+1:
            combined.append(null)
        else:
            combined[-1] = (combined[-1][0], max(combined[-1][1], null[1]))

    return sum(end-start+1 for start, end in combined)

def part2(coords, max_coord=4000000):
    for y in tqdm(range(max_coord+1)):
        nulls = []
        for sensor, beacon in coords:
            dist = manhattan(sensor, beacon)
            row_offset = abs(y-sensor[1])
            if row_offset < dist:
                half_width = dist - row_offset
                start = max(0, sensor[0] - half_width)
                end = min(max_coord, sensor[0] + half_width)
                nulls.append((start, end))

        nulls.sort(key=lambda pt: pt[0])

        # super unlikely edge case
        if nulls[0][0] == 1:
            return y
        if nulls[0][1] == max_coord-1:
            return (max_coord-1) * 4000000 + y

        # merge any overlapping ranges together
        combined = [nulls[0]]
        for null in nulls[1:]:
            if null[0] > combined[-1][1]+1:
                combined.append(null)
            else:
                combined[-1] = (combined[-1][0], max(combined[-1][1], null[1]))

        if len(combined) > 1:
            assert len(combined) == 2
            return (combined[0][1]+1) * 4000000 + y

def parse_input(data_src):
    data_src.seek(0)
    COORD_RE = re.compile(r'x=(-?\d+), y=(-?\d+)')
    coords = [COORD_RE.findall(line) for line in data_src.read().splitlines()]
    coords = [[(int(s[0]), int(s[1])), (int(p[0]), int(p[1]))] for s, p in coords]
    return [coords]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data), y=10) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 5040643

        assert part2(*parse_input(test_data), max_coord=20) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (26, 56000011)
    TEST_INPUT = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
