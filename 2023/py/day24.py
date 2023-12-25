#!/usr/bin/env python3
import itertools
import time
from collections import namedtuple
from io import StringIO

import sympy as sp

Position = namedtuple('Position', ['x', 'y', 'z'])
Velocity = namedtuple('Velocity', ['x', 'y', 'z'])
StateVector = namedtuple('StateVector', ['pos', 'vel'])

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None, None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def part1(hail, bounds=(200000000000000, 400000000000000)):
    count = 0
    for stone1, stone2 in itertools.combinations(hail, 2):
        x, y = line_intersection((stone1.pos, (stone1.pos.x+stone1.vel.x, stone1.pos.y+stone1.vel.y)),
                                 (stone2.pos, (stone2.pos.x+stone2.vel.x, stone2.pos.y+stone2.vel.y)))

        if x is None:
            continue

        dx = x - stone1.pos.x
        dy = y - stone1.pos.y
        if (dx > 0) != (stone1.vel.x > 0) or (dy > 0) != (stone1.vel.y > 0):
            continue

        dx = x - stone2.pos.x
        dy = y - stone2.pos.y
        if (dx > 0) != (stone2.vel.x > 0) or (dy > 0) != (stone2.vel.y > 0):
            continue

        if bounds[0] <= x <= bounds[1] and bounds[0] <= y <= bounds[1]:
            count += 1

    return count

def part2(hail):
    # need to solve the following equation:
    #   x0+t*vx0 + y0+t*vy0 + z0+t*vz0 = xi+t*vxi + yi+t*vyi + zi+t*vzi
    #
    # since any solution that works for all lines in the input should also work
    # for any three lines (that aren't parallel) we don't need to check against
    # every line in the input - just try 3 of them. if the input doesn't converge
    # try 3 different ones.
    #
    #   x0+t0*vx0 - x1-t0*vx1 = 0
    #   y0+t0*vy0 - y1-t0*vy1 = 0
    #   z0+t0*vz0 - z1-t0*vz1 = 0
    #
    #   x0+t1*vx0 - x2-t1*vx2 = 0
    #   y0+t1*vy0 - y2-t1*vy2 = 0
    #   z0+t1*vz0 - z2-t1*vz2 = 0
    #
    #   x0+t2*vx0 - x3-t2*vx3 = 0
    #   y0+t2*vy0 - y3-t2*vy3 = 0
    #   z0+t2*vz0 - z3-t2*vz3 = 0
    #
    # this is also a good excuse to try out sympy

    x0 = sp.Symbol('x0')
    y0 = sp.Symbol('y0')
    z0 = sp.Symbol('z0')
    vx0 = sp.Symbol('vx0')
    vy0 = sp.Symbol('vy0')
    vz0 = sp.Symbol('vz0')
    t = sp.symbols('t0:3')

    system = []
    for i, stone in enumerate(hail[:3]):
        system.append(x0 + t[i]*vx0 - stone.pos.x - t[i]*stone.vel.x)
        system.append(y0 + t[i]*vy0 - stone.pos.y - t[i]*stone.vel.y)
        system.append(z0 + t[i]*vz0 - stone.pos.z - t[i]*stone.vel.z)

    solution = sp.solve_poly_system(system, x0, y0, z0, vx0, vy0, vz0, *t)
    return sum(solution[0][:3])

def parse_input(data_src):
    data_src.seek(0)
    hail = []
    for line in data_src.read().splitlines():
        p, v = line.split('@')
        pos = Position(*map(int, p.strip().split(', ')))
        vel = Velocity(*map(int, v.strip().split(', ')))
        hail.append(StateVector(pos, vel))
    return [hail]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data), (7, 27)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 15262

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 695832176624149

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (2, 47)
    TEST_INPUT = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
