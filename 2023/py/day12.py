#!/usr/bin/env python3
import functools
import time
from io import StringIO


def count_arrangements(arr, groups):
    @functools.cache
    def dfs(idx, group, run):
        if idx == len(arr):
            return (group == len(groups) and run == 0 or
                    group == len(groups)-1 and run == groups[-1])
        total = 0

        # check if starting/continuing a run
        if arr[idx] in '#?' and group < len(groups) and run < groups[group]:
            total += dfs(idx+1, group, run+1)

        # check if ending a run or no run in progress
        if arr[idx] in '.?' and (run == 0 or run == groups[group]):
            total += dfs(idx+1, group+bool(run), 0)

        return total
    return dfs(0, 0, 0)

def part1(springs):
    return sum(count_arrangements(*spring) for spring in springs)

def part2(springs):
    big_springs = [['?'.join([arr]*5), groups*5] for arr, groups in springs]
    return sum(count_arrangements(*spring) for spring in big_springs)

def parse_input(data_src):
    data_src.seek(0)
    springs = []
    for line in data_src.read().splitlines():
        arr, groups = line.split()
        groups = list(map(int, groups.split(',')))
        springs.append([arr, groups])
    return [springs]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 7506

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 548241300348335

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (21, 525152)
    TEST_INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
