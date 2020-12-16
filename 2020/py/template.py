#!/usr/bin/env python3

def part1():
    pass

def part2():
    pass

def parse_input(lines):
    for line in lines:
        pass
    return parsed

def run_tests():
    test_input = """
""".strip().split('\n')
    parsed = parse_input(test_input)
    # assert part1(parsed _input) == 165

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    parsed = parse_input(test_input)
    print(f"Part 1: {part1(parsed)}")
    print(f"Part 2: {part2(parsed)}")
