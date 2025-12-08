#!/usr/bin/env python3
import itertools
import math
import time
import typing
from io import StringIO


def part1(boxes, num_pairs=1000):
    dists = [(a, b, math.dist(a, b)) for a, b in itertools.combinations(boxes, 2)]
    dists.sort(key = lambda x: x[2])

    circuit_map = {box: frozenset([box]) for box in boxes}
    for i in range(num_pairs):
        a, b, _ = dists[i]
        circuit_a = circuit_map[a]
        circuit_b = circuit_map[b]
        new_circuit = frozenset(circuit_a | circuit_b)
        for circuit in new_circuit:
            circuit_map[circuit] = new_circuit

    unique = frozenset()
    for s in circuit_map.values():
        unique = frozenset(unique | {s})

    ordered = sorted([len(circuit) for circuit in unique])
    return math.prod(ordered[-3:])

def part2(boxes):
    dists = [(a, b, math.dist(a, b)) for a, b in itertools.combinations(boxes, 2)]
    dists.sort(key = lambda x: x[2])

    circuit_map = {box: frozenset([box]) for box in boxes}
    for a, b, _ in dists:
        circuit_a = circuit_map[a]
        circuit_b = circuit_map[b]
        new_circuit = frozenset(circuit_a | circuit_b)
        if len(new_circuit) == len(boxes):
            return a[0] * b[0]
        for circuit in new_circuit:
            circuit_map[circuit] = new_circuit

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    boxes = []
    for line in data_src.read().splitlines():
        boxes.append(tuple(map(int, line.split(','))))
    return [boxes]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data), num_pairs=10)
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=75680)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=None)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
    TEST_ANSWER1 = 40

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 25272

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
