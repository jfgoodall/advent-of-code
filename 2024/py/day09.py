#!/usr/bin/env python3
import time
import typing
from io import StringIO

try:
    pass
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable


def part1(disk_map):
    checksum = 0
    fwd_id = 0
    rev_id = len(disk_map) // 2
    fwd_idx = 0
    rev_idx = len(disk_map) - 1
    block_position = 0

    while fwd_idx <= rev_idx:
        if fwd_idx % 2 == 0:
            # fill forwards
            checksum += block_position * fwd_id

            disk_map[fwd_idx] -= 1
            if disk_map[fwd_idx] == 0:
                fwd_idx += 1
        else:
            # check for 0 empty blocks
            if disk_map[fwd_idx] == 0:
                fwd_idx += 1
                fwd_id += 1
                continue

            # fill backwards
            checksum += block_position * rev_id

            disk_map[fwd_idx] -= 1
            if disk_map[fwd_idx] == 0:
                fwd_idx += 1
                fwd_id += 1

            disk_map[rev_idx] -= 1
            if disk_map[rev_idx] == 0:
                rev_idx -= 2
                rev_id -= 1

        block_position += 1

    return checksum

def part2(disk_map):
    # pre-process disk map into data structures: [pos, size, [id]]
    space_blocks = []
    file_blocks = [[0, disk_map[0], 0]]
    pos = disk_map[0]
    file_id = 1
    for idx in range(1, len(disk_map), 2):
        space_blocks.append([pos, disk_map[idx]])
        pos += disk_map[idx]
        file_blocks.append([pos, disk_map[idx+1], file_id])
        pos += disk_map[idx+1]
        file_id += 1

    for fb in reversed(file_blocks):
        for sp in space_blocks:
            # don't move files to the right
            if fb[0] < sp[0]:
                break

            # move a file if it fits
            if fb[1] <= sp[1]:
                fb[0] = sp[0]
                sp[0] += fb[1]
                sp[1] -= fb[1]
                break

    checksum = 0
    for fb in file_blocks:
        checksum += fb[2] * sum(range(fb[0], fb[0]+fb[1]))

    return checksum

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    return [list(map(int, data_src.read().strip()))]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile))  # 6331212425418

        my_part2_answer = part2(*parse_input(test2_data))
        assert my_part2_answer == test2_answer, f"got {my_part2_answer}; should be {test2_answer}"
        solve_part('2', part2, *parse_input(infile))  # 6363268339304

def solve_part(part_label: str, part_fn: typing.Callable, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
2333133121414131402
"""
    TEST_ANSWER1 = 1928

    TEST_INPUT2 = TEST_INPUT1
    TEST_ANSWER2 = 2858

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
