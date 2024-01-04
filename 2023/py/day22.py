#!/usr/bin/env python3
import time
from collections import defaultdict
from copy import deepcopy
from io import StringIO

import numpy as np
from tqdm import tqdm


def map_blocks(blocks):
    block_to_pts = {}
    pt_to_block = {}
    for block_id, block in blocks.items():
        delta = np.sign(block[1] - block[0])
        pts = []
        pt = block[0].copy()
        while True:
            pts.append(tuple(pt))
            pt_to_block[tuple(pt)] = block_id
            if np.array_equal(pt, block[1]):
                break
            pt += delta
        block_to_pts[block_id] = pts

    return block_to_pts, pt_to_block

def apply_gravity(block_to_pts, pt_to_block):
    count = 0
    for block_id, _ in sorted(block_to_pts.items(),
                              key=lambda x: min(p[2] for p in x[1])):
        fell = False
        while True:
            pts = block_to_pts[block_id]
            for pt in pts:
                block_below = pt_to_block.get((pt[0], pt[1], pt[2]-1))
                if (block_below and block_below != block_id) or pt[2] == 1:
                    # this block cannot fall further
                    break
            else:
                # drop block by 1
                new_pts = []
                for pt in pts:
                    new_pt = (pt[0], pt[1], pt[2]-1)
                    del pt_to_block[pt]
                    pt_to_block[new_pt] = block_id
                    new_pts.append(new_pt)
                block_to_pts[block_id] = new_pts
                fell = True
                continue  # check if this block can continue falling
            break  # go to next block
        count += fell
    return count

def calc_supports(pt_to_block):
    supports = defaultdict(set)
    supported_by = defaultdict(set)
    for pt, block_id in pt_to_block.items():
        if above := pt_to_block.get((pt[0], pt[1], pt[2]+1)):
            if above != block_id:
                supports[block_id].add(above)

        if below := pt_to_block.get((pt[0], pt[1], pt[2]-1)):
            if below != block_id:
                supported_by[block_id].add(below)
    return supports, supported_by

def disintegratable_blocks(blocks, supports, supported_by):
    # count disintegratable blocks
    disintegratable = set()
    for block_id in blocks:
        for overhead in supports[block_id]:
            if not (supported_by[overhead] - {block_id}):
                break
        else:
            disintegratable.add(block_id)
    return disintegratable

def part1(blocks):
    block_to_pts, pt_to_block = map_blocks(blocks)
    apply_gravity(block_to_pts, pt_to_block)
    supports, supported_by = calc_supports(pt_to_block)
    return len(disintegratable_blocks(blocks.keys(), supports, supported_by))

def part2(blocks):
    block_to_pts, pt_to_block = map_blocks(blocks)
    apply_gravity(block_to_pts, pt_to_block)
    supports, supported_by = calc_supports(pt_to_block)
    safe = disintegratable_blocks(blocks.keys(), supports, supported_by)

    count = 0
    for block_id in tqdm(set(blocks)-safe):
        b2p = deepcopy(block_to_pts)
        p2b = pt_to_block.copy()

        for pt in b2p[block_id]:
            del p2b[pt]
        del b2p[block_id]

        # todo: turn disintegratable_blocks() into a recursive function that returns the number of
        # blocks to fall given a block_id - can be used for part1 also
        count += apply_gravity(b2p, p2b)

    return count

def parse_input(data_src):
    data_src.seek(0)
    blocks = {}
    for block_id, line in enumerate(data_src.read().splitlines(), start=1):
        a, b = line.split('~')
        a = np.fromiter(map(int, a.split(',')), dtype=int)
        b = np.fromiter(map(int, b.split(',')), dtype=int)
        blocks[block_id] = a, b
    return [blocks]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # -

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (5, 7)
    TEST_INPUT = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
