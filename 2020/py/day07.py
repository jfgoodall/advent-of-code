#!/usr/bin/env python3
from functools import lru_cache

class hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))

@lru_cache(maxsize=None)
def holds_color(rules, bag_color, target_color):
    holds = rules[bag_color]
    if target_color in holds:
        return True
    for held_color in holds:
        if holds_color(rules, held_color, target_color):
            return True
    return False

def solve_part1(rules):
    holds_gold = set()
    for bag_color in rules:
        if holds_color(rules, bag_color, 'shiny gold'):
            holds_gold.add(bag_color)
    return len(holds_gold)

@lru_cache(maxsize=None)
def count_held(rules, bag_color):
    total_count = 0
    for bag, count in rules[bag_color].items():
        total_count += count * (count_held(rules, bag) + 1)
    return total_count

def solve_part2(rules):
    return count_held(rules, 'shiny gold')

def parse_input(lines):
    """ creates a dict of dicts: rules[color] = {'color': count, ...} """
    import re
    rule_re = re.compile(r'(\d+ ?)?(\w+ \w+) bags?')
    rules = hashabledict()
    for line in lines:
        matches = rule_re.findall(line)
        rule_label = matches[0][1]
        rule = hashabledict()
        for pair_idx in range(1, len(matches)):
            count, label = matches[pair_idx]
            if count:
                rule[label] = int(count)
        rules[rule_label] = rule
    return rules

def test_solve():
    test_input = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip()
    rules = parse_input(test_input.split('\n'))
    assert solve_part1(rules) == 4
    assert solve_part2(rules) == 32

if __name__ == '__main__':
    test_solve()
    with open('day07-input.dat') as infile:
        test_input = parse_input(infile)
    print(f"Part 1: {solve_part1(test_input)}")
    print(f"Part 2: {solve_part2(test_input)}")
