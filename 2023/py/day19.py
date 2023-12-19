#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import time
from copy import deepcopy
from dataclasses import dataclass, field
from io import StringIO


@dataclass
class Rule:
    category: str
    comparison: str
    value: int
    workflow: str

def part1(workflows, parts):
    total = 0
    for part in parts:
        wf = 'in'
        while True:
            if wf in 'AR':
                if wf == 'A':
                    total += sum(part.values())
                break

            for rule in workflows[wf]:
                if (rule.comparison == '<' and part[rule.category] < rule.value or
                    rule.comparison == '>' and part[rule.category] > rule.value):
                    wf = rule.workflow
                    break
            else:
                wf = rule.workflow
    return total

def part2(workflows, _):
    """tree time"""
    @dataclass
    class Node:
        workflow: str
        ranges: map[str:tuple[int,int]]
        parent: Node=None
        children: list[Node]=field(default_factory=lambda: [])

    seen = set()
    def grow_tree(node):
        print(node.workflow, node.parent.workflow if node.parent else '', node.ranges)
        if node.workflow in 'AR':
            return

        assert node.workflow not in seen
        seen.add(node.workflow)

        rolling_ranges = deepcopy(node.ranges)
        for rule in workflows[node.workflow]:
            ranges = deepcopy(rolling_ranges)

            if rule.category:
                lower, upper = ranges[rule.category]
                if rule.comparison == '>' and rule.value > ranges[rule.category][0]:
                    ranges[rule.category] = (rule.value+1, upper)
                elif rule.comparison == '<' and rule.value < ranges[rule.category][1]:
                    ranges[rule.category] = (lower, rule.value-1)

                # invert the rolling ranges for the next loop iteration to
                # reflect that the previous rule didn't apply
                lower, upper = ranges[rule.category]
                if rule.comparison == '>':
                    rolling_ranges[rule.category] = (lower, min(rule.value, upper))
                elif rule.comparison == '<':
                    rolling_ranges[rule.category] = (max(rule.value, lower), upper)

            child = Node(rule.workflow, ranges, node)
            node.children.append(child)
            grow_tree(child)

    accepted = []
    def count_accepted(node):
        if node.workflow == 'A':
            accepted.append(node)
            return math.prod(b-a for a, b in node.ranges.values())
        else:
            return sum(count_accepted(child) for child in node.children)


    root = Node('in', {'x':(1,4000), 'm':(1,4000), 'a':(1,4000), 's':(1,4000)})
    grow_tree(root)
    total = count_accepted(root)

    print()
    for node in accepted:
        print(node.parent.workflow, node.ranges)

    # we're overcounting so we probably need to merge overlapping ranges somehow
    # for a, b in itertools.combinations(accepted, 2):
    #     for key in 'xmas':
    #         if b.ranges[key][0] > a.ranges[key][1] or a.ranges[key][0] > b.ranges[key][1]:
    #             break
    #     else:
    #         # :(
    #         print(a.ranges)
    #         print(b.ranges)
    #         print()

    print(total)
    return total

def parse_input(data_src):
    data_src.seek(0)
    workflows_str, parts_str = data_src.read().strip().split('\n\n')

    workflows = {}
    for line in workflows_str.splitlines():
        match = re.match(r"(\w+)\{(.+)}", line)
        name, rules_str = match.groups()
        rules_str = rules_str.split(',')
        rules = []
        for rule in rules_str[:-1]:
            match = re.match(r"([xmas])([><])(\d+):(\w+)", rule)
            cat, comp, val, wf = match.groups()
            rules.append(Rule(cat, comp, int(val), wf))
        rules.append(Rule(None, None, None, rules_str[-1]))
        workflows[name] = rules

    parts = []
    for line in parts_str.splitlines():
        part = {}
        for category in line[1:-1].split(','):
            key, val = category.split('=')
            part[key] = int(val)
        parts.append(part)

    return [workflows, parts]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 397643

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (19114, 167409079868000)
    TEST_INPUT = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
