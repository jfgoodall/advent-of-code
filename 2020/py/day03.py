#!/usr/bin/env python3

def solve(matrix, right, down):
    tile_height = len(matrix)
    tile_width = len(matrix[0])
    x_pos, y_pos = 0, 0
    tree_count = 0
    while y_pos < tile_height:
        if matrix[y_pos][x_pos] == '#':
            tree_count += 1
        x_pos = (x_pos + right) % tile_width
        y_pos += down
    return tree_count

def test_solve():
    test_input = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip().split('\n')
    assert solve(test_input, 3, 1) == 7

if __name__ == '__main__':
    test_solve()
    with open('day03-input.dat') as infile:
        matrix = [line.strip() for line in infile]
    print(f"Part 1: {solve(matrix, 3, 1)}")

    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for slope in slopes:
        product *= solve(matrix, *slope)
    print(f"Part 2: {product}")
