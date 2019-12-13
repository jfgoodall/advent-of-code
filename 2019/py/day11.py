#/usr/bin/env python3
from collections import defaultdict
from enum import Enum
import operator
from intcode_cpu import IntcodeCPU

class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

def turn(direction, code):
    if code == 0:  # turn left
        if direction == Direction.UP: return Direction.LEFT
        if direction == Direction.LEFT: return Direction.DOWN
        if direction == Direction.DOWN: return Direction.RIGHT
        if direction == Direction.RIGHT: return Direction.UP
    elif code == 1: # turn right
        if direction == Direction.UP: return Direction.RIGHT
        if direction == Direction.LEFT: return Direction.UP
        if direction == Direction.DOWN: return Direction.LEFT
        if direction == Direction.RIGHT: return Direction.DOWN

def move(position, direction):
    return (position[0]+direction.value[0],
            position[1]+direction.value[1])

def paint_hull(memory, starting_color):
    position = (0, 0)
    direction = Direction.UP
    colors = defaultdict(int)
    colors[position] = starting_color

    cpu = IntcodeCPU()
    cpu.load_program(memory)
    while not cpu.halted():
        output = cpu.continue_program([colors[position]])
        colors[position] = output[0]
        direction = turn(direction, output[1])
        position = move(position, direction)

    return colors

with open('day11.dat') as f:
    memory = f.readlines()
    assert len(memory) == 1
    memory = list(map(int, memory[0].strip().split(',')))

colors = paint_hull(memory, 0)
print("part 1: {}".format(len(colors)))

colors = paint_hull(memory, 1)
x_extents = (min(colors.keys(), key=operator.itemgetter(0))[0],
             max(colors.keys(), key=operator.itemgetter(0))[0])
y_extents = (min(colors.keys(), key=operator.itemgetter(1))[1],
             max(colors.keys(), key=operator.itemgetter(1))[1])
width = x_extents[1] - x_extents[0] + 1
height = y_extents[1] - y_extents[0] + 1
# print('width: {}, height: {}'.format(width, height))

raster = [[u'\u2591' for _ in range(width)] for _ in range(height)]
for coord, color in colors.items():
    x = coord[0]-x_extents[0]
    y = coord[1]-y_extents[0]
    if color == 1:
        raster[y][x] = u'\u2588'

print("part 2:")
for line in reversed(raster):
    print(''.join(line))
