#!/usr/bin/env python3

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def coords(self):
        return (self.x, self.y)

def rotate(facing, direction, degrees):
    TURN_MAP = {'N': 0, 'E': 1, 'S': 2, 'W': 3, 3: 'W', 2: 'S', 1: 'E', 0: 'N'}
    d = TURN_MAP[facing]
    if direction == 'R':
        d += degrees // 90
    else:
        d -= degrees // 90
    return TURN_MAP[d%4]

def rotate_point(point, direction, degrees):
    turns = degrees // 90
    if direction == 'L':
        turns = (4 - turns) % 4
    rotated = Position(point.x, point.y)
    for _ in range(turns):
        rotated = Position(rotated.y, -rotated.x)
    return rotated

def part1(movements):
    pos = Position()
    facing = 'E'
    for movement in movements:
        op, arg = movement
        if op == 'N':
            pos.y += arg
        elif op == 'E':
            pos.x += arg
        elif op == 'S':
            pos.y -= arg
        elif op == 'W':
            pos.x -= arg
        elif op == 'R' or op == 'L':
            facing = rotate(facing, op, arg)
        elif op == 'F':
            if facing == 'N':
                pos.y += arg
            elif facing == 'E':
                pos.x += arg
            elif facing == 'S':
                pos.y -= arg
            elif facing == 'W':
                pos.x -= arg
        else:
            assert False
    return pos

def part2(movements):
    ship = Position()
    waypoint = Position(10, 1)
    for movement in movements:
        op, arg = movement
        if op == 'N':
            waypoint.y += arg
        elif op == 'E':
            waypoint.x += arg
        elif op == 'S':
            waypoint.y -= arg
        elif op == 'W':
            waypoint.x -= arg
        elif op == 'R' or op == 'L':
            waypoint = rotate_point(waypoint, op, arg)
        elif op == 'F':
            ship.x += arg * waypoint.x
            ship.y += arg * waypoint.y
        else:
            assert False
    return ship

def parse_input(lines):
    return [(l[0], int(l[1:])) for l in lines]

def run_tests():
    assert rotate('N', 'R', 90) == 'E'
    assert rotate('N', 'R', 180) == 'S'
    assert rotate('N', 'R', 270) == 'W'
    assert rotate('N', 'R', 360) == 'N'
    assert rotate('N', 'L', 90) == 'W'
    assert rotate('N', 'L', 180) == 'S'
    assert rotate('N', 'L', 270) == 'E'
    assert rotate('N', 'L', 360) == 'N'
    assert rotate_point(Position(2, 0), 'R', 90).coords() == (0, -2)
    assert rotate_point(Position(2, 0), 'L', 90).coords() == (0, 2)
    assert rotate_point(Position(2, 0), 'R', 180).coords() == (-2, 0)
    test_input = """
F10
N3
F7
R90
F11
""".strip().split('\n')
    movements = parse_input(test_input)
    pos = part1(movements)
    assert abs(pos.x) + abs(pos.y) == 25
    pos = part2(movements)
    assert abs(pos.x) + abs(pos.y) == 286

if __name__ == '__main__':
    run_tests()
    with open('day12-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    movements = parse_input(test_input)
    pos = part1(movements)
    print(f"Part 1: {abs(pos.x) + abs(pos.y)}")
    pos = part2(movements)
    print(f"Part 2: {abs(pos.x) + abs(pos.y)}")
