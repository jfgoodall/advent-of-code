#!/usr/bin/env python3
import itertools
import time
import typing
from collections import defaultdict
from io import StringIO


def find_groups(links):
    networks = defaultdict(set)
    for a, b in links:
        networks[a].add(a)
        networks[a].add(b)
        networks[b].add(a)
        networks[b].add(b)

    all_groups = set()
    for linked_pair in links:
        group = set(linked_pair)
        neighbors = list(linked_pair)
        seen =  set()
        while neighbors:
            cpu = neighbors.pop()
            if cpu in seen:
                continue
            seen.add(cpu)

            if all(cpu in networks[g] and g in networks[cpu] for g in group):
                group.add(cpu)
                neighbors.extend(list(networks[cpu]))

        all_groups.add(tuple(sorted(group)))

    return all_groups

def part1(links):
    groups = find_groups(links)

    triples = set()
    for group in groups:
        if len(group) == 3:
            triples.add(group)
        elif len(group) > 3:
            # break down larger groups into groups of 3
            for g in itertools.combinations(group, 3):
                triples.add(tuple(g))

    count = 0
    for group in triples:
        count += int(any(cpu[0] == 't' for cpu in group))
    return count

def part2(links):
    groups = find_groups(links)
    max_group = max(groups, key=lambda g: len(g))
    return ','.join(max_group)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    links = []
    for line in data_src.read().splitlines():
        links.append(tuple(line.split('-')))
    return [links]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=1077)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile),
                   expected="bc,bf,do,dw,dx,ll,ol,qd,sc,ua,xc,yu,zt")

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
    TEST_ANSWER1 = 7

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = "co,de,ka,ta"

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
