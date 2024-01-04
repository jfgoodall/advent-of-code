#!/usr/bin/env python3

def part1(ranges, tickets):
    all_valid = {v for r in ranges.values() for v in r}
    return sum(val for ticket in tickets for val in ticket if val not in all_valid)

def part2(ranges, tickets):
    from contextlib import suppress

    # remove invalid tickets
    all_valid = {v for r in ranges.values() for v in r}
    bad_tickets = []
    for i, ticket in enumerate(tickets):
        if any(val not in all_valid for val in ticket):
            bad_tickets.append(i)
    for idx in reversed(bad_tickets):
        del tickets[idx]

    # create a matrix of possible indices for each field
    matrix = {field: list(range(len(tickets[0]))) for field in ranges}

    # eliminate indices where ticket values are invalid
    for field_idx in range(len(tickets[0])):
        xsection = [t[field_idx] for t in tickets]
        for field, f_range in ranges.items():
            if not all(v in f_range for v in xsection):
                matrix[field].remove(field_idx)

    # eliminate indices which are solutions for other fields, sudoku-style
    used = set()
    while any(len(possible) > 1 for possible in matrix.values()):
        for target_field, indices in matrix.items():
            if len(indices) == 1 and indices[0] not in used:
                target_index = indices[0]
                used.add(target_index)
                break
        for field in matrix:
            if field != target_field:
                with suppress(ValueError):
                    matrix[field].remove(target_index)

    # finally...solve the problem
    product = 1
    for field, index in matrix.items():
        if field.startswith('departure'):
            product *= tickets[0][index[0]]
    return product

def parse_input(document):
    import re
    RANGE_RE = re.compile(r'^(.+): (\d+)-(\d+) or (\d+)-(\d+)$')
    sections = document.split('\n\n')
    ranges = {}
    for line in sections[0].split('\n'):
        m = RANGE_RE.match(line.strip())
        v = list(map(int, m.groups()[1:]))
        ranges[m.groups()[0]] = set(range(v[0], v[1]+1)) | set(range(v[2], v[3]+1))
    tickets = []
    tickets.append(list(map(int, sections[1].split('\n')[1].split(','))))
    for line in sections[2].split('\n')[1:]:
        tickets.append(list(map(int, line.split(','))))
    return ranges, tickets

def run_tests():
    test_input = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""".strip()
    ranges, tickets = parse_input(test_input)
    assert part1(ranges, tickets) == 71

    test_input = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""".strip()
    ranges, tickets = parse_input(test_input)
    part2(ranges, tickets)

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip()
    ranges, tickets = parse_input(test_input)
    print(f"Part 1: {part1(ranges, tickets)}")
    print(f"Part 2: {part2(ranges, tickets)}")
