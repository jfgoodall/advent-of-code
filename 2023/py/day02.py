#!/usr/bin/env python3
import time
from collections import defaultdict
from io import StringIO


def part1(games):
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14

    total = 0
    for gid, game in games.items():
        r = max(rnd['red'] for rnd in game)
        g = max(rnd['green'] for rnd in game)
        b = max(rnd['blue'] for rnd in game)
        if r <= MAX_RED and g <= MAX_GREEN and b <= MAX_BLUE:
            total += gid
    return total

def part2(games):
    total = 0
    for game in games.values():
        r = max(rnd['red'] for rnd in game)
        g = max(rnd['green'] for rnd in game)
        b = max(rnd['blue'] for rnd in game)
        total += r * g * b
    return total

def parse_input(data_src):
    data_src.seek(0)
    games = {}
    for line in data_src.read().splitlines():
        game_str, rounds_str = line.split(':')
        gid = int(game_str.split(' ')[1])

        rounds = []
        for this_round in rounds_str.split(';'):
            cubes = defaultdict(int)
            for cube in this_round.split(','):
                num, color = cube.strip().split(' ')
                cubes[color] = int(num)
            rounds.append(cubes)
        games[gid] = rounds

    return [games]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 3059

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 65371

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (8, 2286)
    TEST_INPUT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
