#!/usr/bin/env python3

def print_grid(grid, grid_width):
    num_rows = len(grid) // grid_width
    grid_str = ''.join(grid)
    for line in (grid_str[i*grid_width:(i+1)*grid_width] for i in range(num_rows)):
        print(line)
    print()

def get_seat(grid, grid_width, x, y):
    width = grid_width
    height = len(grid) // grid_width
    if x < 0 or x >= width or y < 0 or y >= height:
        return None
    return grid[y*width+x]

def iterate_grid(grid, grid_width):
    from collections import defaultdict
    new_grid = ['.'] * len(grid)
    for idx, seat in enumerate(grid):
        if seat == '.':
            continue
        y = idx // grid_width
        x = idx % grid_width
        adjacent = defaultdict(int)
        for pos in ((x-1, y-1), (x, y-1), (x+1, y-1),
                    (x-1, y),             (x+1, y),
                    (x-1, y+1), (x, y+1), (x+1, y+1)):
            adjacent[get_seat(grid, grid_width, *pos)] += 1
        if seat == 'L' and adjacent['#'] == 0:
            new_grid[idx] = '#'
        elif seat == '#' and adjacent['#'] >= 4:
            new_grid[idx] = 'L'
        else:
            new_grid[idx] = seat
    return new_grid

def iterate_grid_extended(grid, grid_width):
    from collections import defaultdict
    new_grid = ['.'] * len(grid)
    for idx, seat in enumerate(grid):
        if seat == '.':
            continue
        y = idx // grid_width
        x = idx % grid_width
        adjacent = defaultdict(int)
        for direction in ((-1, -1), (0, -1), (+1, -1),
                          (-1, 0),           (+1, 0),
                          (-1, +1), (0, +1), (+1, +1)):
            pos = (x, y)
            while True:
                pos = (pos[0]+direction[0], pos[1]+direction[1])
                next_seat = get_seat(grid, grid_width, *pos)
                if next_seat is None:
                    break
                elif next_seat == 'L' or next_seat == '#':
                    adjacent[next_seat] += 1
                    break
        if seat == 'L' and adjacent['#'] == 0:
            new_grid[idx] = '#'
        elif seat == '#' and adjacent['#'] >= 5:
            new_grid[idx] = 'L'
        else:
            new_grid[idx] = seat
    return new_grid

def iterate_until_stable(grid, grid_width, extended=False):
    while True:
        if extended:
            new_grid = iterate_grid_extended(grid, grid_width)
        else:
            new_grid = iterate_grid(grid, grid_width)
        # print_grid(grid, grid_width)
        if new_grid == grid:
            return new_grid
        grid = new_grid

def count_occupied_seats(grid):
    from collections import Counter
    return Counter(grid)['#']

def parse_input(lines):
    grid_width = lines.find('\n')
    grid = lines.replace('\n', '')
    return list(grid), grid_width

def run_tests():
    test_input = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""".strip()
    grid, grid_width = parse_input(test_input)
    assert count_occupied_seats(iterate_until_stable(grid, grid_width)) == 37
    assert count_occupied_seats(iterate_until_stable(grid, grid_width, extended=True)) == 26

if __name__ == '__main__':
    run_tests()
    with open('day11-input.dat') as infile:
        lines = infile.read().strip()
    grid, grid_width = parse_input(lines)
    print(f"Part 1: {count_occupied_seats(iterate_until_stable(grid, grid_width))}")
    print(f"Part 2: {count_occupied_seats(iterate_until_stable(grid, grid_width, extended=True))}")
