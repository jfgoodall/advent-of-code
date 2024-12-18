#!/usr/bin/env python3
import heapq
import time
import typing


class Node:
    __slots__ = 'pos', 'dist', 'prev', 'obselete'

    def __init__(self, pos, dist, prev):
        # pos: tuple[x, y]
        self.pos = pos
        self.dist = dist
        self.prev: Node = prev
        self.obselete = False

    def __lt__(self, other):
        return self.dist < other.dist

def dijkstra(obstacles, size) -> Node:
    heap = []
    visited = {}

    def add_node(pos, dist, prev: Node):
        if (
            pos[0] < 0 or pos[0] > size or
            pos[1] < 0 or pos[1] > size or
            pos in obstacles
        ):
            return

        if old_node := visited.get(pos):
            old_node.obselete = True

        node = Node(pos, dist, prev)
        heapq.heappush(heap, node)
        visited[pos] = node

    add_node((0, 0), 0, None)
    while heap:
        current = heapq.heappop(heap)

        if current.obselete:
            continue

        if current.pos == (size, size):
            return current

        x, y = current.pos
        for next_pos, next_dist in (
            ((x, y+1), current.dist+1),
            ((x, y-1), current.dist+1),
            ((x+1, y), current.dist+1),
            ((x-1, y), current.dist+1),
        ):
            seen = visited.get(next_pos)
            if not seen or next_dist < seen.dist:
                add_node(next_pos, next_dist, current)

def part1(bytes):
    goal = dijkstra(set(bytes[:1024]), 70)
    return goal.dist

def part2(bytes):
    # invert check and find when path becomes unblocked; the path finder
    # completes faster when there are no valid paths
    obstacles = set(bytes)
    first_blocked = bytes[-1]
    for obstacle in reversed(bytes[:-1]):
        if dijkstra(obstacles, 70):
            return f"{first_blocked[0]},{first_blocked[1]}"

        obstacles.remove(obstacle)
        first_blocked = obstacle

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    bytes = []
    for line in data_src.read().splitlines():
        bytes.append(tuple(map(int, line.split(','))))
    return [bytes]

def main():
    with open(__file__[:-3] + '-input.dat') as infile:
        solve_part('1', part1, *parse_input(infile))  # 340
        solve_part('2', part2, *parse_input(infile))  # 34,32

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    main()
