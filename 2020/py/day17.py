#!/usr/bin/env python3

def active_neighbors(space, coord):
    from itertools import product
    extents = (range(coord[axis]-1, coord[axis]+2) for axis in range(len(coord)))
    active = sum(space.get(neigh, 0) for neigh in product(*extents))
    return active - space.get(coord, 0)  # only count neighbors

def iterate_space(space, dimensions):
    from itertools import product
    # check 1 beyond existing bounds
    extents = (range(min(space, key=lambda coord: coord[axis])[axis]-1,
                     max(space, key=lambda coord: coord[axis])[axis]+2)
               for axis in range(dimensions))
    new_space = {}
    for coord in product(*extents):
        active = active_neighbors(space, coord)
        if coord in space:
            if active in (2, 3):
                new_space[coord] = True
        elif active == 3:
            new_space[coord] = True
    return new_space

def solve(space, dimensions):
    for _ in range(6):
        space = iterate_space(space, dimensions)
    return len(space)

def parse_input(grid, dimensions):
    space = {}
    zeros = (0,) * (dimensions-2)
    for y, row in enumerate(grid.split('\n')):
        for x, state in enumerate(row):
            if state == '#':
                space[(x, y, *zeros)] = True
    return space

def run_tests():
    test_input = """
.#.
..#
###
""".strip()
    space = parse_input(test_input, 3)
    assert solve(space, 3) == 112
    space = parse_input(test_input, 4)
    assert solve(space, 4) == 848

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip()
    space = parse_input(test_input, 3)
    print(f"Part 1: {solve(space, 3)}")
    space = parse_input(test_input, 4)
    print(f"Part 2: {solve(space, 4)}")
