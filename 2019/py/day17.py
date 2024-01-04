#/usr/bin/env python3
from intcode_cpu import IntcodeCPU
from functools import total_ordering
from enum import Enum


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


_TURN_MAP = {
    # start: (back, left, right)
    Direction.NORTH: (Direction.SOUTH, Direction.WEST, Direction.EAST),
    Direction.SOUTH: (Direction.NORTH, Direction.EAST, Direction.WEST),
    Direction.WEST: (Direction.EAST, Direction.SOUTH, Direction.NORTH),
    Direction.EAST: (Direction.WEST, Direction.NORTH, Direction.SOUTH)
}

def turn_back(direction):
    return Direction(_TURN_MAP[direction][0])

def turn_left(direction):
    return Direction(_TURN_MAP[direction][1])

def turn_right(direction):
    return Direction(_TURN_MAP[direction][2])


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


def is_intersection(plot, coord: Coord):
    paths = 0
    for direction in Direction:
        if plot[coord.row][coord.col] != ord('.'):
            try:
                c = coord.move(direction)
                if c.row < 0 or c.col < 0:
                    raise IndexError
                if plot[c.row][c.col] != ord('.'):
                    paths += 1
            except IndexError:
                pass
    return paths > 2


def print_plot(plot):
    for line in plot:
        print(''.join(map(chr, line)))


def find_turn(plot, loc, direction):
    # try turning left
    try:
        c = loc.move(turn_left(direction))
        if c.row >= 0 and c.col >= 0 and plot[c.row][c.col] != ord('.'):
            return (turn_left(direction), 'L')
    except IndexError:
        pass

    # try turning right
    try:
        c = loc.move(turn_right(direction))
        if c.row >= 0 and c.col >= 0 and plot[c.row][c.col] != ord('.'):
            return (turn_right(direction), 'R')
    except IndexError:
        pass

    # dead end
    return (None, None)


def count_steps(plot, loc, direction):
    steps = 0
    try:
        while plot[loc.row][loc.col] != ord('.') and loc.row >= 0 and loc.col >= 0:
            loc = loc.move(direction)
            steps += 1
    except IndexError:
        pass
    loc = loc.move(turn_back(direction))
    steps -= 1
    return (steps, loc)


def find_starting_position(plot):
    ARROW_MAP = {
        ord('^'): Direction.NORTH,
        ord('v'): Direction.SOUTH,
        ord('<'): Direction.WEST,
        ord('>'): Direction.EAST
    }
    loc = None
    facing = None
    for row in range(len(plot)):
        for col in range(len(plot[0])):
            if is_intersection(plot, Coord(row, col)):
                plot[row][col] = ord('O')
            try:
                facing = ARROW_MAP[plot[row][col]]
                loc = Coord(row, col)
                return (loc, facing)
            except KeyError:
                pass
    raise Exception("Shouldn't get here")


def find_full_path(plot):
    loc, facing = find_starting_position(plot)
    full_path = []
    while True:
        facing, label = find_turn(plot, loc, facing)
        if not facing:
            break
        steps, loc = count_steps(plot, loc, facing)
        full_path.append((label, steps))
    return full_path


cpu = IntcodeCPU()
mem = cpu.load_memory_from_file('day17.dat')
output = cpu.run_program(mem)
while output[-1] == ord('\n'):
    output = output[:-1]

width = output.index(ord('\n'))
plot = [output[i:i+width] for i in range(0, len(output), width+1)]
height = len(plot)

alignment_parameter = 0
for row in range(height):
    for col in range(width):
        if is_intersection(plot, Coord(row, col)):
            plot[row][col] = ord('O')
            alignment_parameter += row * col
# print_plot(plot)

print("part 1: {}".format(alignment_parameter))
assert alignment_parameter == 3448

test_plot = """
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
"""
test_plot = list(map(ord, test_plot.strip()))
width = test_plot.index(ord('\n'))
test_plot = [test_plot[i:i+width] for i in range(0, len(test_plot), width+1)]

full_path = find_full_path(test_plot)
# print_plot(test_plot)
# print(full_path)

print_plot(plot)
full_path = find_full_path(plot)
print(full_path)
print(set(full_path))
print(len(set(full_path)))

tuple_map = {}
letter = 'a'
for i in sorted(list(set(full_path))):
    tuple_map[i] = letter
    letter = chr(ord(letter)+1)

print(tuple_map)
mapped_path = ''.join(map(lambda x: tuple_map[x], full_path))
print(mapped_path)

def serialize_substr(substr):
    serialized = ''
    for letter in substr:
        for key, val in tuple_map.items():
            if val == letter:
                turn_step = key
        serialized += turn_step[0] + ',' + str(turn_step[1]) + ','
    return serialized[:-1]

def strip_blank_entries(lst):
    return [i for i in lst if i]

def find_candidate_fns(mapped_path):
    fn_list = []
    for l in range(2, len(mapped_path)+1):
        substr = mapped_path[:l]
        idx = 0
        count = 0
        try:
            while True:
                count += 1
                idx = mapped_path.index(substr, idx+len(substr))
        except ValueError:
            pass
        if (len(serialize_substr(substr)) <= 20):
            fn_list.append(substr)
    return fn_list

fn_a_list = find_candidate_fns(mapped_path)
for fn_a in fn_a_list:
    print('A: {}'.format(fn_a))
    mapped_path_lvl2 = strip_blank_entries(mapped_path.split(fn_a))
    fn_b_list = find_candidate_fns(mapped_path_lvl2[0])
    for fn_b in fn_b_list:
        print('B: {}'.format(fn_b))
        mapped_path_lvl3 = [strip_blank_entries(fn.split(fn_b)) for fn in mapped_path_lvl2]
        mapped_path_lvl3 = [item for sublist in mapped_path_lvl3 for item in sublist]

        fn_c_list = find_candidate_fns(mapped_path_lvl3[0])
        for fn_c in fn_c_list:
            print('C: {}'.format(fn_c))
            mapped_path_lvl4 = [strip_blank_entries(fn.split(fn_c)) for fn in mapped_path_lvl3]
            mapped_path_lvl4 = [item for sublist in mapped_path_lvl4 for item in sublist]
            print(mapped_path_lvl4)
            if not mapped_path_lvl4:
                break
    print()

print()
print("A: {}, B: {}, C: {}".format(fn_a, fn_b, fn_c))
print()

main_routine = ''
idx = 0
while True:
    for fn, label in ((fn_a, 'A'), (fn_b, 'B'), (fn_c, 'C')):
        try:
            if mapped_path[idx:].index(fn) == 0:
                main_routine += label + ','
                idx += len(fn)
                break
        except:
            pass
    if idx == len(mapped_path):
        main_routine = main_routine[:-1]
        break
print("main: {}".format(main_routine))
print("A: {}".format(serialize_substr(fn_a)))
print("B: {}".format(serialize_substr(fn_b)))
print("C: {}".format(serialize_substr(fn_c)))

def str_to_ascii_list(s):
    return [ord(x) for x in s+'\n']

cpu = IntcodeCPU()
mem = cpu.load_memory_from_file('day17.dat')
mem[0] = 2
print(mem[:5])
output = cpu.run_program(mem)
if cpu.halted:
    print('halted')
# print(cpu.continue_program(str_to_ascii_list(main_routine)))
# print(cpu.continue_program(str_to_ascii_list(serialize_substr(fn_a))))
# print(cpu.continue_program(str_to_ascii_list(serialize_substr(fn_b))))
# print(cpu.continue_program(str_to_ascii_list(serialize_substr(fn_c))))

