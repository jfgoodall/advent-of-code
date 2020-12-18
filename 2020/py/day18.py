#!/usr/bin/env python3

def part1(exprs):
    import operator
    OP_MAP = {'+': operator.add, '*': operator.mul}

    def get_operator(expr):
        if expr and expr[0] in ('+', '*'):
            return expr[0], expr[1:]
        return None, expr

    def get_operand(expr):
        if expr[0] == '(':
            balance = 1
            idx = 1
            while balance > 0:
                if expr[idx] == '(':
                    balance += 1
                elif expr[idx] == ')':
                    balance -= 1
                idx += 1
            subexpr = evaluate(expr[1:idx-1])
            return subexpr, expr[idx:]
        else:
            for idx, ch in enumerate(expr):
                if not ch.isdigit():
                    idx -= 1
                    break
            return int(expr[:idx+1]), expr[idx+1:]

    def evaluate(expr):
        result = 0
        op = '+'
        while op:
            val, expr = get_operand(expr)
            result = OP_MAP[op](result, val)
            op, expr = get_operator(expr)
        return result

    assert evaluate('12') == 12
    assert evaluate('1+2*3+4*5+6') == 71
    assert evaluate('2*3+(4*5)') == 26
    assert evaluate('5+(8*3+9+3*4*3)') == 437
    assert evaluate('5*9*(7*3*3+9*3+(8+6*4))') == 12240
    assert evaluate('((2+4*9)*(6+9*8+6)+6)+2+4*2') == 13632

    return sum(evaluate(expr.replace(' ', '')) for expr in exprs)


class RDParser:
    """ grammar:    input := {ws} product {ws} eof
                  product := {ws} sum [{{ws} '*' sum}]
                      sum := {ws} subexpr [{{ws} '+' subexpr}]
                  subexpr := {ws} '(' {ws} product {ws} ')'
                           | number
                   number := \d+
                       ws := \s+
    """
    import re
    TOKEN_RE = re.compile(r"""(?P<whitespace>\s+)|
                              (?P<int>\d+)|
                              (?P<add>\+)|
                              (?P<mul>\*)|
                              (?P<open_paren>\()|
                              (?P<close_paren>\))""", re.VERBOSE)

    def __init__(self, line):
        self.lexer = self.tokenize(line.strip())
        self.token = None

    def tokenize(self, expr):
        for match in self.TOKEN_RE.finditer(expr):
            for token_type, token_str in match.groupdict().items():
                if token_type != 'whitespace' and token_str:
                    yield token_type, token_str
                    break
        yield 'eof', None

    def next_token(self):
        while True:
            self.token = next(self.lexer)
            if self.token[0] != 'whitespace':
                break

    def parse(self):
        self.next_token()
        result = self.parse_product()
        assert self.token[0] == 'eof'
        return result

    def parse_product(self):
        result = self.parse_sum()
        while self.token[0] == 'mul':
            self.next_token()
            result *= self.parse_sum()
        return result

    def parse_sum(self):
        result = self.parse_subexpr()
        while self.token[0] == 'add':
            self.next_token()
            result += self.parse_subexpr()
        return result

    def parse_subexpr(self):
        if self.token[0] == 'open_paren':
            self.next_token()
            result = self.parse_product()
            assert self.token[0] == 'close_paren'
            self.next_token()
            return result
        else:
            assert self.token[0] == 'int'
            result = int(self.token[1])
            self.next_token()
            return result

def part2(exprs):
    assert RDParser('1 + 2 * 3 + 4 * 5 + 6').parse() == 231
    assert RDParser('1 + (2 * 3) + (4 * (5 + 6))').parse() == 51
    assert RDParser('2 * 3 + (4 * 5)').parse() == 46
    assert RDParser('5 + (8 * 3 + 9 + 3 * 4 * 3)').parse() == 1445
    assert RDParser('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))').parse() == 669060
    assert RDParser('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2').parse() == 23340

    return sum(RDParser(expr).parse() for expr in exprs)

if __name__ == '__main__':
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    print(f"Part 1: {part1(test_input)}")
    print(f"Part 2: {part2(test_input)}")
