#!/usr/bin/env python3
import time, itertools, functools, heapq
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
from dataclasses import dataclass
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

COST_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000, '.': 0,
            1: 'A', 10: 'B', 100: 'C', 1000: 'D', 0: '.'}

@dataclass(frozen=True)
class GameState:
    hall: tuple = ((0,)*11)  # hallway, left to right
    rooms: tuple = (((0,0),)*4)  # rooms, left to right, top to bottom

    def __str__(self):
        hall = ''.join(COST_MAP[self.hall[i]] for i in range(len(self.hall)))
        rooms = [' '.join(COST_MAP[room[j]] for room in self.rooms) for j in range(len(self.rooms[0]))]
        return '\n  '.join([hall] + rooms)

HALL_GOAL = {1: 2, 10: 4, 100: 6, 1000: 8}
ROOM_GOAL = {0: 1, 1: 10, 2: 100, 3: 1000}
HALL_IDX = {0: 2, 1: 4, 2: 6, 3: 8}
ROOM_IDX = {1: 0, 10: 1, 100: 2, 1000: 3}
HALL_STOPS = {0, 1, 3, 5, 7, 9, 10}

def find_hall_moves(state):
    """return list of (state, cost) moves"""
    moves = []

    open_slots = []
    for room in range(len(state.rooms)):
        for slot in range(len(state.rooms[room])-1, -1, -1):
            if state.rooms[room][slot] == 0:
                open_slots.append(slot)
                break
            elif state.rooms[room][slot] != ROOM_GOAL[room]:
                open_slots.append(None)
                break
        else:
            open_slots.append(None)

    # hall to room moves
    for i in range(11):
        if pod := state.hall[i]:
            hall_goal = HALL_GOAL[pod]
            room_goal = state.rooms[ROOM_IDX[pod]]

            # check if there's space in the goal room
            slot = open_slots[ROOM_IDX[pod]]
            if slot is not None:

                #check if there's space in the hall to move to the room
                start, end = (i+1, hall_goal+1) if i < hall_goal else (hall_goal, i)
                if all(state.hall[h] == 0 for h in range(start, end)):
                    cost = pod * (abs(i-hall_goal) + slot + 1)
                    new_hall = list(state.hall)
                    new_hall[i] = 0
                    new_room = list(room_goal)
                    new_room[slot] = pod
                    new_state = GameState(hall=tuple(new_hall),
                                          rooms=tuple(r if r!=room_goal else tuple(new_room)
                                                      for r in state.rooms))
                    moves.append((new_state, cost))
    return moves

def find_room_moves(state):
    """return list of (state, cost) moves"""
    moves = []

    # room to hall moves
    for j in range(4):
        # only check the top occupied slot in each room
        for slot in range(len(state.rooms[j])):
            if state.rooms[j][slot]:
                break
        else:
            continue

        pod = state.rooms[j][slot]
        if j == ROOM_IDX[pod] and all(state.rooms[j][s] == pod
                                      for s in range(slot, len(state.rooms[j]))):
            continue  # in the right place already

        hall_dest = []
        for h in range(HALL_IDX[j]+1, 11):
            if state.hall[h]:
                break
            if h in HALL_STOPS:
                hall_dest.append(h)
        for h in range(HALL_IDX[j]-1, -1, -1):
            if state.hall[h]:
                break
            if h in HALL_STOPS:
                hall_dest.append(h)

        if not hall_dest:
            continue

        new_room = list(state.rooms[j])
        new_room[slot] = 0
        new_rooms = tuple(state.rooms[x] if x!=j else tuple(new_room) for x in range(4))
        for h in hall_dest:
            cost = pod * (abs(h-HALL_IDX[j]) + slot + 1)
            new_hall = list(state.hall)
            new_hall[h] = pod
            new_state = GameState(hall=tuple(new_hall),
                                  rooms=new_rooms)
            moves.append((new_state, cost))
    return moves

def find_all_moves(state):
    """return list of (state, cost) moves"""
    return find_hall_moves(state) + find_room_moves(state)

class Node:
    __slots__ = 'state', 'cost', 'fscore', 'removed'

    def __init__(self, state, cost):
        self.state = state
        self.cost = cost
        self.fscore = self.cost + self.h()
        self.removed = False

    def __lt__(self, other):
        return self.fscore < other.fscore

    def h(self):
        extra = 0
        for h, pod in enumerate(self.state.hall):
            if pod:
                extra += pod * (abs(h-HALL_GOAL[pod])+1)
        for r, room in enumerate(self.state.rooms):
            for slot, pod in enumerate(room):
                if pod and pod != ROOM_GOAL[r]:
                    extra += pod * (abs(HALL_IDX[r]-HALL_IDX[ROOM_IDX[pod]])+slot+2)
        return extra

def a_star(state, goal_state):
    heap = []
    state_map = {}

    def add_node(state, cost):
        node = Node(state, cost)
        state_map[state] = node
        heapq.heappush(heap, node)

    add_node(state, 0)
    while heap:
        current = heapq.heappop(heap)
        if current.removed:
            continue
        if current.state == goal_state:
            break
        next_moves = find_all_moves(current.state)
        for move, cost in next_moves:
            if move in state_map:
                if current.cost+cost < state_map[move].cost:
                    state_map[move].removed = True
                    add_node(move, current.cost+cost)
            else:
                add_node(move, current.cost+cost)

    return state_map[goal_state].cost

def part1(state):
    goal = GameState(rooms=((1, 1),(10,10),(100,100),(1000,1000)))
    return a_star(state, goal)

def part2(state):
    state = GameState(hall=state.hall, rooms = (
        (state.rooms[0][0], COST_MAP['D'], COST_MAP['D'], state.rooms[0][1]),
        (state.rooms[1][0], COST_MAP['C'], COST_MAP['B'], state.rooms[1][1]),
        (state.rooms[2][0], COST_MAP['B'], COST_MAP['A'], state.rooms[2][1]),
        (state.rooms[3][0], COST_MAP['A'], COST_MAP['C'], state.rooms[3][1])))
    goal = GameState(rooms=((1,)*4,(10,)*4,(100,)*4,(1000,)*4))
    return a_star(state, goal)

def parse_input(data_src):
    data_src.seek(0)
    next(data_src)
    h_str = next(data_src)
    r_str = (next(data_src), next(data_src))
    hall = tuple(COST_MAP[h_str[i]] for i in range(1, 12))
    rooms = tuple((COST_MAP[r_str[0][i]], COST_MAP[r_str[1][i]]) for i in range(3, 10, 2))
    return GameState(hall=hall, rooms=rooms)

def run_tests():
    TEST_INPUT = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 12521
    assert part2(parse_input(test_data)) == 44169

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 10321
        print_result('2', part2, parse_input(infile))  # 46451
