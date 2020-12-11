#!/usr/bin/env python3

def get_distribution(ratings):
    from collections import Counter
    ordered = sorted(ratings+[0])
    ordered.append(ordered[-1]+3)
    distribution = Counter(p[1]-p[0] for p in zip(ordered, ordered[1:]))
    return (distribution[1], distribution[2], distribution[3])

def calc_combos(ratings):
    from functools import reduce
    ordered = sorted(ratings+[0])
    ordered.append(ordered[-1]+3)
    diffs = [p[1]-p[0] for p in zip(ordered, ordered[1:])]
    runs_of_ones = [0]
    for d in diffs:
        if d == 1:
            runs_of_ones[-1] += 1
        else:
            runs_of_ones.append(0)

    COMBOS = (1, 1, 2, 4, 7)  # calc'd by hand; input data doesn't have runs > 4
    return reduce(lambda x, y: x*COMBOS[y], runs_of_ones, 1)

def parse_input(lines):
    return [int(line.strip()) for line in lines]

def test_get_distribution():
    test_input = """16\n10\n15\n5\n1\n11\n7\n19\n6\n12\n4""".strip()
    ratings = parse_input(test_input.split('\n'))
    assert get_distribution(ratings) == (7, 0, 5)
    assert calc_combos(ratings) == 8

    test_input = """
28\n33\n18\n42\n31\n14\n46\n20\n48\n47\n24\n23\n49\n45\n19\n38\n39\n11\n1\n32\n25\n35\n8\n17\n7\n9\n4\n2\n34\n10\n3
""".strip()
    ratings = parse_input(test_input.split('\n'))
    assert get_distribution(ratings) == (22, 0, 10)
    assert calc_combos(ratings) == 19208

if __name__ == '__main__':
    test_get_distribution()
    with open('day10-input.dat') as infile:
        ratings = parse_input(infile)
    distr = get_distribution(ratings)
    print(f"Part 1: {distr[0]*distr[2]}")
    print(f"Part 2: {calc_combos(ratings)}")
