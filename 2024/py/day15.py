#!/usr/bin/env python3
import time
import typing
from io import StringIO


def travel(grid, move, pos):
    # walk forwards until we hit a space or a wall
    ahead = pos[0]+move[0], pos[1]+move[1]
    while (here := grid[ahead[0]][ahead[1]]) != '.':
        if here == '#':
            return pos
        ahead = ahead[0]+move[0], ahead[1]+move[1]

    # walk back to start moving boxes as we go
    while ahead != pos:
        prev = ahead[0]-move[0], ahead[1]-move[1]
        grid[ahead[0]][ahead[1]] = grid[prev[0]][prev[1]]
        ahead = prev

    grid[ahead[0]][ahead[1]] = '.'
    return pos[0]+move[0], pos[1]+move[1]

def calc_gps(grid):
    gps = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == 'O' or ch == '[':
                gps += 100 * r + c
    return gps

def part1(grid, moves, pos):
    grid = [list(row) for row in grid]

    for move in moves:
        pos = travel(grid, move, pos)

    return calc_gps(grid)

def part2(grid, moves, pos):
    grid = [
        list(
            row.replace('#', '##').
                replace('.', '..').
                replace('O', '[]').
                replace('@', '@.')
        )
        for row in grid
    ]
    pos = pos[0], pos[1]*2

    def box_coord(r, c):
        """get coordinate of left side of a box"""
        return (r, c) if grid[r][c] == '[' else (r, c-1)

    for move in moves:
        if move[0] == 0 or grid[pos[0]+move[0]][pos[1]] == '.':
            pos = travel(grid, move, pos)
        elif grid[pos[0]+move[0]][pos[1]+move[1]] != '#':
            assert move[1] == 0

            # find boxes to move
            box_stack = [box_coord(pos[0]+move[0], pos[1])]
            boxes = []
            while box_stack:
                box = box_stack.pop()
                boxes.append(box)
                if (
                    grid[box[0]+move[0]][box[1]] == '#' or
                    grid[box[0]+move[0]][box[1]+1] == '#'
                ):
                    boxes.clear()
                    break

                ahead = box[0]+move[0], box[1]
                if grid[ahead[0]][ahead[1]] in '[]':
                    box_stack.append(box_coord(*ahead))
                if grid[ahead[0]][ahead[1]+1] == '[':
                    box_stack.append(box_coord(ahead[0], ahead[1]+1))

            # move boxes
            for box in sorted(boxes, reverse=move[0]>0):
                grid[box[0]][box[1]] = '.'
                grid[box[0]][box[1]+1] = '.'
                grid[box[0]+move[0]][box[1]] = '['
                grid[box[0]+move[0]][box[1]+1] = ']'

            # move robot
            if boxes:
                grid[pos[0]][pos[1]] = '.'
                pos = pos[0]+move[0], pos[1]
                grid[pos[0]][pos[1]] = '@'

    return calc_gps(grid)


def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    grid_lines, moves_lines = data_src.read().split('\n\n')
    grid = []
    for r, row in enumerate(grid_lines.split('\n')):
        grid.append(row)
        if (c := row.find('@')) >= 0:
            pos = r, c

    VECTORS = {
        '<': (0, -1),
        '>': (0, 1),
        '^': (-1, 0),
        'v': (1, 0)
    }
    moves = []
    for move in moves_lines.replace('\n', ''):
        moves.append(VECTORS[move])

    return [grid, moves, pos]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 1451928

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 1462788

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
    TEST_ANSWER1 = 10092

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 9021

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
