#!/usr/bin/env python3
from collections import defaultdict

NEIGHBORS = ((1, 0), (1, -1), (0, 1), (-1, 0), (0, -1), (-1, 1))
WHITE = False
BLACK = True

def adjacent_black(space, coord):
    """ return number of adjacent black tiles """
    return sum(space[(coord[0]+n[0], coord[1]+n[1])] for n in NEIGHBORS)

def init_space(paths):
    space = defaultdict(bool)
    for path in paths:
        x, y = 0, 0
        for offset in path:
            x += offset[0]
            y += offset[1]
        space[(x, y)] = not space[(x, y)]
    return space

def part1(paths):
    space = init_space(paths)
    return sum(space.values())

def iterate_space(space):
    from itertools import product
    # check 1 beyond existing bounds
    extents = (range(min(space, key=lambda coord: coord[axis])[axis]-1,
                     max(space, key=lambda coord: coord[axis])[axis]+2)
               for axis in range(2))
    new_space = defaultdict(bool)
    for coord in product(*extents):
        b = adjacent_black(space, coord)
        if space[coord] == BLACK:
            if b == 0 or b > 2:
                new_space[coord] = WHITE
            else:
                new_space[coord] = BLACK
        else:
            if b == 2:
                new_space[coord] = BLACK
    return new_space

def part2(paths):
    space = init_space(paths)
    for _ in range(100):
        space = iterate_space(space)
    return sum(space.values())

def parse_input(lines):
    import re
    DIR_RE = re.compile(r'(e)|(se)|(ne)|(w)|(nw)|(sw)')
    DIR_MAP = {'e': (1, 0), 'se': (1, -1), 'ne': (0, 1), 'w': (-1, 0), 'sw': (0, -1), 'nw': (-1, 1)}
    paths = []
    for line in lines:
        offsets = [DIR_MAP[m.group()] for m in DIR_RE.finditer(line.strip())]
        paths.append(offsets)
    return paths

def run_tests():
    test_input = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""".strip().split('\n')
    paths = parse_input(test_input)
    assert part1(paths) == 10
    assert part2(paths) == 2208

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    paths = parse_input(test_input)
    print(f"Part 1: {part1(paths)}")
    print(f"Part 2: {part2(paths)}")
