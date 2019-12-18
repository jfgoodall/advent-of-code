#/usr/bin/env python3
from intcode_cpu import IntcodeCPU
from enum import Enum
from functools import total_ordering
import curses

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    @classmethod
    def opposite(cls, direction):
        if direction == cls.NORTH:
            return cls.SOUTH
        elif direction == cls.SOUTH:
            return cls.NORTH
        elif direction == cls.WEST:
            return cls.EAST
        else:  # direction == cls.EAST:
            return cls.WEST


@total_ordering
class Coord:
    """ Row/Column notation for coordinate with (0,0) being top-left """
    def __init__(self, row, col):
        self._coord = (row, col)

    def __repr__(self):
        return str(self._coord)

    def __getitem__(self, key):
        return self._coord[key]

    def __lt__(self, other):
        if self[0] < other[0]:
            return True
        else:
            return self[1] < other[1]

    def __eq__(self, other):
        return self._coord == other._coord

    def __hash__(self):
        return hash(self._coord)

    @property
    def row(self):
        return self[0]

    @property
    def col(self):
        return self[1]

    def move(self, direction: Direction):
        if direction == Direction.NORTH:
            return Coord(self.row-1, self.col)
        elif direction == Direction.SOUTH:
            return Coord(self.row+1, self.col)
        elif direction == Direction.WEST:
            return Coord(self.row, self.col-1)
        else:  # direction == Direction.EAST:
            return Coord(self.row, self.col+1)


class Node:
    class NodeType(Enum):
        WALL = 0
        OPEN = 1
        TARGET = 2

    def __init__(self, coord: Coord, tile_type: NodeType):
        self._coord = coord
        self._tile_type = tile_type
        self._oxygenated = False

    def __repr__(self):
        return str((self._coord, self._tile_type))

    def __hash__(self):
        return hash(self._coord)

    @property
    def coord(self):
        return self._coord

    @property
    def tile_type(self):
        return self._tile_type

    @property
    def oxygenated(self):
        return self._oxygenated

    @oxygenated.setter
    def oxygenated(self, value):
        self._oxygenated = value


def get_tile_type(coord):
    if coord._coord == (2, 2):
        return Node.NodeType.TARGET
    elif coord.row <= 0 or coord.row >= 3 or coord.col <= 0 or coord.col >= 5:
        return Node.NodeType.WALL
    else:
        return Node.NodeType.OPEN


def crawl():
    cpu = IntcodeCPU()
    memory = cpu.load_memory_from_file('day15.dat')
    cpu.load_program(memory)

    def move_droid(direction):
        output = cpu.continue_program([direction.value])
        assert not cpu.halted()
        return Node.NodeType(output[0])

    start = Node(Coord(1, 1), Node.NodeType.OPEN)
    nodes = {start.coord: start}
    stack = [[1, None]]
    here = start.coord
    while stack:
        next_move = stack.pop()
        # print("@ {}, going {}".format(here, Direction(next_move[0]).name if next_move[0]<5 else 'back'), end='')
        if next_move[0] == 5:
            if stack:
                move_direction = Direction.opposite(Direction(next_move[1]))
                here = here.move(move_direction)
                node_type = move_droid(move_direction)
                assert here in nodes
                assert nodes[here].tile_type != Node.NodeType.WALL
                assert nodes[here].tile_type == node_type
            # print()
            continue

        move_direction = Direction(next_move[0])
        next_loc = here.move(move_direction)
        next_node = Node(next_loc, move_droid(move_direction))
        # print(' --> {}'.format(next_node), end='')

        next_move[0] += 1
        stack.append(next_move)

        if next_loc in nodes:
            # print('  already visited', end='')
            if next_node.tile_type != Node.NodeType.WALL:
                back_dir = Direction.opposite(Direction(next_move[0]-1))
                move_droid(back_dir)
                # print('  backing out {} to {}'.format(back_dir, here), end='')
            # print()
            continue

        nodes[next_node.coord] = next_node
        if next_node.tile_type != Node.NodeType.WALL:
            here = next_node.coord
            stack.append([1, next_move[0]-1])
        # print()
    return nodes

nodes = crawl()
nodes = {c: n for c, n in nodes.items() if n.tile_type != Node.NodeType.WALL}

def get_neighbors(here, exclude=None):
    neighbors = [nodes.get(here.move(direction), None)
                 for direction in Direction]
    return [n.coord for n in neighbors
            if n is not None and (exclude is None or n.coord != exclude)]

def steps_to_target(start, prev):
    steps = 0
    n = get_neighbors(start, prev)
    here = start
    while len(n) == 1:
        steps += 1
        tmp = get_neighbors(n[0], here)
        here = n[0]
        n = tmp

    if len(n) == 0:
        if nodes[here].tile_type != Node.NodeType.TARGET:
            steps += 10000000
        return steps
    else:
        return steps + min([steps_to_target(neighbor, here) for neighbor in n]) + 1


steps = steps_to_target(Coord(1, 1), None)
print("part 1: {}".format(steps))
assert steps == 246


def nodes_without_o2():
    return [n for n in nodes if not nodes[n].oxygenated]


for n in nodes:
    if nodes[n].tile_type == Node.NodeType.TARGET:
        nodes[n].oxygenated = True
airless = nodes_without_o2()
minutes = 0
while airless:
    adjacent = []
    for n in airless:
        neighbors = get_neighbors(n)
        if any([nodes[i].oxygenated for i in neighbors]):
            adjacent.append(n)

    for n in adjacent:
        nodes[n].oxygenated = True

    airless = nodes_without_o2()
    minutes += 1
print("part 2: {}".format(minutes))
assert minutes == 376






def draw_map(stdscr):
    if not curses.has_colors():
        raise Exception('no colors')
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    # for i in range(curses.COLORS):
    #     curses.init_pair(i+1, i, -1)
    stdscr.clear()
    curses.noecho()
    curses.curs_set(False)
    stdscr.refresh()

    min_row = min([node.coord.row for node in nodes.values()])
    min_col = min([node.coord.col for node in nodes.values()])
    height = max([node.coord.row for node in nodes.values()]) - min_row + 1
    width = max([node.coord.col for node in nodes.values()]) - min_col + 1

    pad = curses.newpad(100, 100)
    for row in range(height):
        pad.addstr(row, 0, ' '*width, curses.color_pair(1)|curses.A_REVERSE)
    pad.addstr(height, 0, '{} rows x {} cols'.format(height, width))

    for node in nodes.values():
        row = node.coord.row - min_row
        col = node.coord.col - min_col
        if node.tile_type == Node.NodeType.OPEN:
            pad.addch(row, col, ' ')
        elif node.tile_type == Node.NodeType.TARGET:
            pad.addch(row, col, '*')
    pad.addch(1-min_row, 1-min_col, '@')
    pad.refresh(0, 0, 0, 0, height, width)

    stdscr.getkey()

# curses.wrapper(draw_map)

