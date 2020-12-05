#!/usr/bin/env python3
from collections import defaultdict

def solve(code):
    row = 0
    for char in code[:7]:
        row = row * 2
        if char == 'B':
            row = row + 1
    col = 0
    for char in code[7:]:
        col = col * 2
        if char == 'R':
            col = col + 1
    seat = row * 8 + col
    return row, col, seat

def test_solve():
    assert solve("BFFFBBFRRR") == (70, 7, 567)
    assert solve("FFFBBBFRRR") == (14, 7, 119)
    assert solve("BBFFBBFRLL") == (102, 4, 820)

if __name__ == '__main__':
    test_solve()
    with open('day05-input.dat') as infile:
        seats = [solve(line.strip()) for line in infile]

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
