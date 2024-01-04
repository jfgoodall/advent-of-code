#!/usr/bin/env python3
import math
import re
import time
from collections import namedtuple
from io import StringIO

Rule = namedtuple('Rule', ['category', 'comparison', 'value', 'workflow'])

EMPTY_RANGE = {ch:(0,-1) for ch in 'xmas'}
WHOLE_RANGE = {ch:(1,4000) for ch in 'xmas'}

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
                    break
            wf = rule.workflow
    return total

def apply_rule(rule, ranges) -> tuple[map, map]:
    passed = ranges.copy()
    rejected = ranges.copy()

    if not rule.category:
        if rule.workflow != 'R':
            rejected = EMPTY_RANGE
        else:
            passed = EMPTY_RANGE
    else:
        lower, upper = ranges[rule.category]
        if (rule.comparison == '<' and upper < rule.value or
            rule.comparison == '>' and lower > rule.value):
            rejected = EMPTY_RANGE
        elif (rule.comparison == '<' and lower >= rule.value or
              rule.comparison == '>' and upper <= rule.value):
            passed = EMPTY_RANGE
        else:
            if rule.comparison == '<':
                passed[rule.category] = (lower, rule.value-1)
                rejected[rule.category] = (rule.value, upper)
            else:
                passed[rule.category] = (rule.value+1, upper)
                rejected[rule.category] = (lower, rule.value)

    return passed, rejected

def count_accepted(workflows, workflow, ranges):
    if workflow == 'A':
        return math.prod(upper-lower+1 for lower, upper in ranges.values())
    elif workflow == 'R':
        return 0

    count = 0
    for rule in workflows[workflow]:
        passed, rejected = apply_rule(rule, ranges)
        count += count_accepted(workflows, rule.workflow, passed)
        ranges = rejected
    return count

def part2(workflows, _):
    return count_accepted(workflows, 'in', WHOLE_RANGE)

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
        print_result('2', part2, *parse_input(infile))  # 132392981697081

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
