#!/usr/bin/env python3
import time
import typing
from dataclasses import dataclass
from functools import cache
from io import StringIO


@dataclass(unsafe_hash=True)
class Node:
    row: int
    col: int
    left = None
    right = None

def build_tree(grid):
    for col, cell in enumerate(grid[0]):
        if cell == 'S':
            break
    for row, line in enumerate(grid):
        if line[col] == '^':
            break
    root = Node(row, col)
    node_map = {(row, col) : root}

    unprocessed_nodes = [root]
    while len(unprocessed_nodes):
        node = unprocessed_nodes.pop()

        for child_str, c in (("left", node.col-1), ("right", node.col+1)):
            r = node.row
            while r < len(grid) - 1 and grid[r][c] != '^':
                r += 1
            if grid[r][c] == '^':
                if child_node := node_map.get((r, c)):
                    setattr(node, child_str, child_node)
                else:
                    new_node = Node(r, c)
                    setattr(node, child_str, new_node)
                    node_map[(r, c)] = new_node
                    unprocessed_nodes.append(new_node)

    return root, node_map

def part1(grid):
    _, node_map = build_tree(grid)
    return len(node_map)

def part2(grid):
    @cache
    def count_paths(node: Node):
        if node:
            return count_paths(node.left) + count_paths(node.right)
        return 1

    root, _ = build_tree(grid)
    return count_paths(root)

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    grid = [list(line) for line in data_src.read().splitlines()]
    return [grid]  # note: return single item as [item] for *parse_input

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=1622)

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, \
            f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile), expected=10357305916520)

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
    TEST_ANSWER1 = 21

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 40

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
