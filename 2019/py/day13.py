#/usr/bin/env python3
from intcode_cpu import IntcodeCPU
from enum import Enum
import itertools

class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    Paddle = 3
    Ball = 4

with open('day13.dat') as f:
    memory = f.readlines()
    assert len(memory) == 1
    memory = list(map(int, memory[0].strip().split(',')))


cpu = IntcodeCPU()
output = cpu.run_program(memory)
block_tiles = [t for t in output[2::3] if Tile(t) == Tile.Block]
print("part 1: {}".format(len(block_tiles)))
assert len(block_tiles) == 348


memory[0] = 2
cpu.load_program(memory)
in_data = []
score = 0
while not cpu.halted():
    output = cpu.continue_program(in_data)
    iterators = [iter(output)] * 3
    for x, y, tile in itertools.zip_longest(*iterators):
        if (x, y) == (-1, 0):
            score = tile
        elif Tile(tile) == Tile.Ball:
            ball_x = x
        elif Tile(tile) == Tile.Paddle:
            paddle_x = x
    if ball_x < paddle_x:
        in_data = [-1]
    elif ball_x > paddle_x:
        in_data = [1]
    else:
        in_data = [0]

print("part 2: {}".format(score))
assert score == 16999

