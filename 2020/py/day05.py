#!/usr/bin/env python3
from collections import defaultdict

def parse_boarding_pass(code):
    import re
    # (B, F, R, L) -> (1, 0, 1, 0)
    code = re.sub(r'.', lambda ch: '1' if ch.group(0) in 'BR' else '0', code.strip())
    seat = int(code, base=2)
    row = seat >> 3
    col = seat & 0b111
    return row, col, seat

def test_parse_boarding_pass():
    assert parse_boarding_pass("BFFFBBFRRR") == (70, 7, 567)
    assert parse_boarding_pass("FFFBBBFRRR") == (14, 7, 119)
    assert parse_boarding_pass("BBFFBBFRLL") == (102, 4, 820)

if __name__ == '__main__':
    test_parse_boarding_pass()
    with open('day05-input.dat') as infile:
        seats = [parse_boarding_pass(line.strip()) for line in infile]

    print(f"Part 1: {max(seats, key=lambda x: x[2])[2]}")

    min_row = min(seats, key=lambda x: x[0])[0]
    max_row = max(seats, key=lambda x: x[0])[0]
    rows = defaultdict(set)
    for seat in seats:
        if seat[0] != min_row and seat[0] != max_row:
            rows[seat[0]].add(seat[1])
    for row, cols in rows.items():
        if len(cols) != 8:
            for c in range(8):
                if c not in cols:
                    print(f"Part 2: {row*8+c}")
                    break
