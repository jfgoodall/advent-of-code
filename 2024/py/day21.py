#!/usr/bin/env python3
import heapq
import itertools
import time
import typing
from functools import cache
from io import StringIO


class Node:
    __slots__ = 'pos', 'dist', 'prev', 'obselete'

    def __init__(self, pos, dist, prev):
        # pos: tuple[row, col]
        self.pos = pos
        self.dist = dist
        self.prev: list[Node] = prev
        self.obselete = False

    def __lt__(self, other):
        return self.dist < other.dist

# using dijkstra to pathfind between buttons because it's already written
def dijkstra(grid, start, end) -> Node:
    # this version finds all equally best paths; returns goal node
    ROWS = len(grid)
    COLS = len(grid[0])

    heap = []
    visited = {}
    goal_node = None

    def add_node(pos, dist, prev: list[Node]):
        if (
            pos[0] < 0 or pos[0] >= ROWS or
            pos[1] < 0 or pos[1] >= COLS or
            grid[pos[0]][pos[1]] == ' '
        ):
            return

        if old_node := visited.get(pos):
            old_node.obselete = True

        node = Node(pos, dist, prev)
        heapq.heappush(heap, node)
        visited[pos] = node

    add_node((start[0], start[1]), 0, [])
    while heap:
        current = heapq.heappop(heap)
        row, col = current.pos

        if (
            current.obselete or
            goal_node and current.dist > goal_node.dist
        ):
            continue

        if (row, col) == end:
            goal_node = current
            continue

        for next_pos, next_dist in (
            ((row, col+1), current.dist+1),
            ((row, col-1), current.dist+1),
            ((row+1, col), current.dist+1),
            ((row-1, col), current.dist+1),
        ):
            seen = visited.get(next_pos)
            if not seen or next_dist <= seen.dist:
                next_prev = [current]
                if seen and next_dist == seen.dist:
                    next_prev.extend(seen.prev)
                add_node(next_pos, next_dist, next_prev)

    return goal_node

def unwind_paths(node: Node, seq=''):
    """get a list of all best button sequence paths"""
    if not node.prev:
        return [seq+'A']  # all paths end with 'A' to push the button

    new_seqs = []
    for p in node.prev:
        match p.pos[0]-node.pos[0], p.pos[1]-node.pos[1]:
            case -1, 0:
                new_seqs += unwind_paths(p, 'v'+seq)
            case 1, 0:
                new_seqs += unwind_paths(p, '^'+seq)
            case 0, 1:
                new_seqs += unwind_paths(p, '<'+seq)
            case 0, -1:
                new_seqs += unwind_paths(p, '>'+seq)
    return new_seqs

def build_button_map(grid):
    coords = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            coords[ch] = r, c
    buttons = [ch for ch in coords if ch != ' ']

    button_map = {}
    for a, b in itertools.combinations_with_replacement(buttons, 2):
        button_map[a,b] = unwind_paths(dijkstra(grid, coords[a], coords[b]))
        button_map[b,a] = unwind_paths(dijkstra(grid, coords[b], coords[a]))
    return button_map

def calc_complexities(codes, num_robots):
    numeric = build_button_map(('789', '456', '123', ' 0A'))
    directional = build_button_map((' ^A', '<v>'))

    @cache
    def min_cost(a, b, num_robots):
        if num_robots == 1:
            return min(len(p) for p in directional[a, b])
        return min(
            sum(min_cost(x, y, num_robots-1) for x, y in itertools.pairwise('A'+p))
            for p in directional[a, b]
        )

    complexities = 0
    for code in codes:
        numeric_subpaths = [numeric[*pair] for pair in itertools.pairwise('A'+code)]
        numeric_paths = [''.join(p) for p in itertools.product(*numeric_subpaths)]

        seq_len = min(
            sum(min_cost(x, y, num_robots-1) for x, y in itertools.pairwise('A'+p))
            for p in numeric_paths
        )
        complexities += seq_len * int(code[:-1])

    return complexities

def part1(codes):
    return calc_complexities(codes, 3)

def part2(codes):
    return calc_complexities(codes, 26)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [data_src.read().splitlines()]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 222670

        solve_part('2', part2, *parse_input(infile))  # 271397390297138

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
029A
980A
179A
456A
379A
"""
    TEST_ANSWER1 = 126384

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = float('nan')

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
