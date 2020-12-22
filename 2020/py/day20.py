#!/usr/bin/env python3
import math

TEST_INPUT = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

def border_matches(b1, b2):
    return b1 == b2 or b1 == ''.join(reversed(b2))

def num_sides(tile):
    return len([m for m in tile['matches'] if m])

def find_matches(tiles):
    for tile in tiles.values():
        mismatched = 0
        matches = []
        for b1_id, border in enumerate(tile['borders']):
            matched = False
            for _id, t2 in tiles.items():
                if t2 is not tile:
                    for b2 in t2['borders']:
                        matched = border_matches(border, b2)
                        if matched:
                            matches.append(_id)
                            break
                if matched: break
            if not matched:
                matches.append(None)
        tile['matches'] = matches

def find_corners(tiles):
    find_matches(tiles)
    return [_id for _id, t in tiles.items() if num_sides(t) == 2]

def part1(tiles):
    from functools import reduce
    corners = find_corners(tiles)
    return reduce(lambda x, y: x*y, corners)

def rotate_tile(tile):
    # clockwise
    image = [[] for _ in range(len(tile['image']))]
    for l in reversed(tile['image']):
        for idx, ch in enumerate(l):
            image[idx].append(ch)
    image = [''.join(l) for l in image]
    m = tile['matches']
    return {'matches': [m[3], m[0], m[1], m[2]],
            'image': image}

def flip_tile(tile, vert=False):
    # horizontally
    if not vert:
        m = tile['matches']
        return {'matches': [m[0], m[3], m[2], m[1]],
                'image': [''.join(reversed(l)) for l in tile['image']]}
    else:
        return rotate_tile(rotate_tile(flip_tile(tile)))

def print_tile(tile):
    for l in tile['image']:
        print(l)

def assemble_tiles(tiles, corner_id):
    # first row, first tile
    left_id = corner_id
    left_t = tiles[left_id]
    left_t = flip_tile(left_t)  # try without this
    while left_t['matches'][0] or left_t['matches'][3]:
        left_t = rotate_tile(left_t)
    tiles[left_id] = left_t

    # first row, remaining tiles
    row = [left_id]
    while left_t['matches'][1]:
        right_id = left_t['matches'][1]
        right_t = tiles[right_id]
        while right_t['matches'][3] != left_id:
            right_t = rotate_tile(right_t)
        if right_t['matches'][0]:
            right_t = flip_tile(right_t, vert=True)
        tiles[right_id] = right_t
        row.append(right_id)
        left_t, left_id = right_t, right_id
    tile_grid = [row]

    for _ in range(int(math.sqrt(len(tiles)))-1):
        # first tile of row
        row_above = tile_grid[-1]
        left_id = tiles[row_above[0]]['matches'][2]
        left_t = tiles[left_id]
        while left_t['matches'][0] != row_above[0]:
            left_t = rotate_tile(left_t)
        if left_t['matches'][3]:
            left_t = flip_tile(left_t)
        tiles[left_id] = left_t

        # remaining tiles of row
        row = [left_id]
        while left_t['matches'][1]:
            right_id = left_t['matches'][1]
            right_t = tiles[right_id]
            while right_t['matches'][3] != left_id:
                right_t = rotate_tile(right_t)
            if right_t['matches'][0] != row_above[len(row)]:
                right_t = flip_tile(right_t, vert=True)
            tiles[right_id] = right_t
            row.append(right_id)
            left_t, left_id = right_t, right_id
        tile_grid.append(row)

    return tile_grid

def assemble_image(tiles, tile_grid):
    tile_size = len(tiles[tile_grid[0][0]]['image'])
    image = []
    for tile_row in tile_grid:
        for row in range(1, tile_size-1):
            line = ''
            for tile in tile_row:
                line += tiles[tile]['image'][row][1:-1]
            image.append(line)
    return image

def rotate_image(image):
    rotated = [[] for _ in range(len(image))]
    for l in reversed(image):
        for idx, ch in enumerate(l):
            rotated[idx].append(ch)
    return [''.join(l) for l in rotated]

def flip_image(image):
    return [''.join(reversed(l)) for l in image]

def print_image(image):
    for l in image:
        print(l)

def part2(tiles):
    import re
    corners = find_corners(tiles)
    tile_grid = assemble_tiles(tiles, corners[0])
    image = assemble_image(tiles, tile_grid)

    hashes = sum(line.count('#') for line in image)

    ABOVE_RE = re.compile(r'(?=..................#.)')
    BODY_RE  = re.compile(r'(?=#....##....##....###)')
    BELOW_RE = re.compile(r'(?=.#..#..#..#..#..#...)')

    for _ in range(2):
        for __ in range(4):
            monsters = 0
            for row in range(1, len(image)-1):
                a = set(m.start() for m in ABOVE_RE.finditer(image[row-1]))
                b = set(m.start() for m in BODY_RE.finditer(image[row]))
                c = set(m.start() for m in BELOW_RE.finditer(image[row+1]))
                monsters += len(set.intersection(a, b, c))
            if monsters:
                return hashes - monsters*15
            image = rotate_image(image)
        image = flip_image(image)

def parse_input(tile_text):
    # tile[id] = {image, borders, matches}
    import re
    TILE_ID_RE = re.compile(r'Tile (\d+):')
    tiles = {}
    for text in tile_text.split('\n\n'):
        lines = text.split('\n')
        tile_id = int(TILE_ID_RE.match(lines[0]).groups()[0])
        image = lines[1:]
        borders = [image[0],
                   ''.join(l[-1] for l in image),
                   ''.join(reversed(image[-1])),
                   ''.join(l[0] for l in reversed(image))]
        tiles[tile_id] = {'borders': borders, 'image': image}

    return tiles

def run_tests():
    tiles = parse_input(TEST_INPUT.strip())
    assert part1(tiles) == 20899048083289

    tiles = parse_input(TEST_INPUT.strip())
    assert part2(tiles) == 273

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip()
    tiles = parse_input(test_input)
    print(f"Part 1: {part1(tiles)}")
    print(f"Part 2: {part2(tiles)}")
