#!/usr/bin/env python3
import heapq
import time
import typing
from io import StringIO


class Node:
    __slots__ = 'pos', 'dist', 'prev', 'obselete'

    def __init__(self, pos, dist, prev):
        # pos: tuple[row, col, d_row, d_col]
        self.pos = pos
        self.dist = dist
        self.prev: list[Node] = prev
        self.obselete = False

    def __lt__(self, other):
        return self.dist < other.dist

def dijkstra(grid, start, end) -> Node:
    # this version finds all equally best paths; returns goal node
    heap = []
    visited = {}
    goal_node = None

    def add_node(pos, dist, prev: list[Node]):
        if grid[pos[0]][pos[1]] == '#':
            return

        if old_node := visited.get(pos):
            old_node.obselete = True

        node = Node(pos, dist, prev)
        heapq.heappush(heap, node)
        visited[pos] = node

    add_node((start[0], start[1], 0, 1), 0, [])
    while heap:
        current = heapq.heappop(heap)
        row, col, drow, dcol = current.pos

        if (
            current.obselete or
            goal_node and current.dist > goal_node.dist
        ):
            continue

        if (row, col) == end:
            goal_node = current
            continue

        for next_pos, next_dist in (
            ((row+drow, col+dcol, drow, dcol), current.dist+1),
            ((row, col, dcol, -drow), current.dist+1000),
            ((row, col, -dcol, drow), current.dist+1000)
        ):
            seen = visited.get(next_pos)
            if not seen or next_dist <= seen.dist:
                next_prev = [current]
                if seen and next_dist == seen.dist:
                    next_prev.extend(seen.prev)
                add_node(next_pos, next_dist, next_prev)

    return goal_node

def part1(grid, start, end):
    goal = dijkstra(grid, start, end)
    return goal.dist

def part2(grid, start, end):
    path_coords = set()
    backtrack = [dijkstra(grid, start, end)]
    while backtrack:
        node = backtrack.pop()
        backtrack.extend(node.prev)
        path_coords.add((node.pos[0], node.pos[1]))
    return len(path_coords)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    grid = []
    for r, row in enumerate(data_src.read().splitlines()):
        grid.append(row)
        if (c := row.find('S')) > 0:
            start = r, c
        if (c := row.find('E')) > 0:
            end = r, c

    return [grid, start, end]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 72428

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 456

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
    TEST_ANSWER1 = 7036

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 45

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
