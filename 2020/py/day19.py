#!/usr/bin/env python3

class RDParser:
    def __init__(self):
        self._rules = {}

    def add_rule(self, rule_str):
        import re
        rule_id, rule_body = rule_str.strip().split(': ')
        rule_id = int(rule_id)
        terminal_match = re.match(r'"([ab])"', rule_body)
        if terminal_match:
            self._rules[rule_id] = self._create_terminal_rule((terminal_match.groups()[0],))
        else:
            subrules = [tuple(map(int, id_group.split())) for id_group in rule_body.split('|')]
            self._rules[rule_id] = self._create_production_rule(subrules)

    def _create_production_rule(self, subrules):
        def rule(idx, expr):
            for sub in subrules:
                offset = idx
                for rule_id in sub:
                    res = self._rules[rule_id](offset, expr)
                    if res is None:
                        break
                    offset = res
                if res is not None:
                    return offset
            return None
        return rule

    def _create_terminal_rule(self, terminal_strs):
        def rule(idx, expr):
            for terminal in terminal_strs:
                if expr[idx:].startswith(terminal):
                    return idx + len(terminal)
            return None
        return rule

    def validate(self, expr):
        return self._rules[0](0, expr) == len(expr)

def part1(parser, data):
    return sum(parser.validate(expr) for expr in data)

def part2(parser, data):
    from itertools import product

    # 8: 42 | 42 8         --> 42{x}       : x>0
    # 11: 42 31 | 42 11 31 --> 42{y} 31{y} : y>0

    valid = 0
    for expr in data:
        for x, y in product(range(1, len(expr)), range(1, len(expr))):
            # parser.add_rule(f'8: {repeat(42, x)}')
            # parser.add_rule(f'11: {repeat(42, y)} {repeat(31, y)}')
            parser._rules[8] = parser._create_production_rule([(42,)*x])
            parser._rules[11] = parser._create_production_rule([(42,)*y + (31,)*y])
            if parser.validate(expr):
                valid += 1
                break
    return valid

def parse_input(lines):
    rules, data = lines.strip().split('\n\n')
    p = RDParser()
    for line in rules.split('\n'):
        p.add_rule(line.strip())
    data = data.split('\n')
    return p, data

def run_tests():
    test_input = """
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
bba
abaa
""".strip()
    parser, data = parse_input(test_input)
    assert [parser.validate(expr) for expr in data] == [True, True, False, False]

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip()
    parser, data = parse_input(test_input)
    print(f"Part 1: {part1(parser, data)}")
    print(f"Part 2: {part2(parser, data)}")
