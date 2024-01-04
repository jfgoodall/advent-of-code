#!/usr/bin/env python3

def solve(starting_nums, nth):
    history = {}
    for t, n in enumerate(starting_nums):
        history[n] = t+1
    t = len(starting_nums)
    nxt = 0

    for t in range(t+1, nth):
        prev_t = history.get(nxt, 0)
        age = t - prev_t if prev_t else prev_t
        history[nxt] = t
        nxt = age
    return nxt

def run_tests():
    test_input = [0, 3, 6]
    assert solve([0, 3, 6], 10) == 0
    assert solve([0, 3, 6], 2020) == 436
    assert solve([1, 3, 2], 2020) == 1

if __name__ == '__main__':
    run_tests()
    starting_nums = [9, 19, 1, 6, 0, 5, 4]
    print(f"Part 1: {solve(starting_nums, 2020)}")
    print(f"Part 2: {solve(starting_nums, 30000000)}")
