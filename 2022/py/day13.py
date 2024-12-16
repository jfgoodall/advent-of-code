#!/usr/bin/env python3
import functools
import time
from io import StringIO


def in_order(left, right):
    # assert not isinstance(left, int) and not isinstance(right, int)
    for l, r in zip(left, right):
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            elif l > r:
                return False
        else:
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            order = in_order(l, r)
            if order is not None:
                return order

    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False

    return None  # ternary option: we don't know yet

def part1(pairs):
    total = 0
    for idx, (left, right) in enumerate(pairs, 1):
        # assert in_order(left, right) is not None
        if in_order(left, right):
            total += idx
    return total

def part2(pairs):
    DIVIDERS = [[[2]], [[6]]]
    packets = [packet for pair in pairs for packet in pair] + DIVIDERS

    packet_sort_key = functools.cmp_to_key(
        lambda left, right: 1 if in_order(left, right) else -1
    )

    packets.sort(key=packet_sort_key, reverse=True)
    return (packets.index(DIVIDERS[0])+1) * (packets.index(DIVIDERS[1])+1)
    # can't use bisect with a key function until Python 3.10 :(
    # return (bisect.bisect_right(packets, DIVIDERS[0], key=packet_sort_key) *
    #         bisect.bisect_right(packets, DIVIDERS[1], key=packet_sort_key))

def parse_input(data_src):
    data_src.seek(0)
    pairs = []
    for pair in data_src.read().split('\n\n'):
        left, right = pair.splitlines()
        pairs.append([eval(left), eval(right)])
    return pairs

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(parse_input(test_data)) == test_answers[0]
        print_result('1', part1, parse_input(infile))  # 5557

        assert part2(parse_input(test_data)) == test_answers[1]
        print_result('2', part2, parse_input(infile))  # 22425

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (13, 140)
    TEST_INPUT = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
