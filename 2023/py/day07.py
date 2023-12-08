#!/usr/bin/env python3
import functools
import time
from collections import Counter
from enum import IntEnum
from io import StringIO

CARDS = '23456789TJQKA'
CARD_VAL = {c: CARDS.index(c)+2 for c in CARDS}
CARDS_J = 'J23456789TQKA'
CARD_VAL_J = {c: CARDS_J.index(c)+1 for c in CARDS}

class Rank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    TRIPS = 4
    FULL_HOUSE = 5
    QUADS = 6
    QUINTS = 7

def hand_val_order(cards):
    vals = tuple(CARD_VAL[c] for c in cards)
    unique = len(set(vals))
    c = Counter(vals)
    if unique == 5:
        rank = Rank.HIGH_CARD
    elif unique == 4:
        return (Rank.ONE_PAIR, vals)
        rank = Rank.ONE_PAIR
    elif unique == 3:
        if c.most_common()[0][1] == 2:
            rank = Rank.TWO_PAIR
        else:
            rank = Rank.TRIPS
    elif unique == 2:
        if c.most_common()[0][1] == 3:
            rank = Rank.FULL_HOUSE
        else:
            rank = Rank.QUADS
    else:
        rank = Rank.QUINTS
    return (rank, vals)

def hand_val_joker(cards):
    # note J has a value of 1
    vals = tuple(CARD_VAL_J[c] for c in cards)
    unique = len(set(vals))
    c = Counter(vals)
    if unique == 5:
        rank = Rank.ONE_PAIR if 1 in vals else Rank.HIGH_CARD
    elif unique == 4:
        rank = Rank.TRIPS if 1 in vals else Rank.ONE_PAIR
    elif unique == 3:
        if c.most_common()[0][1] == 2:
            if c.most_common()[0][0] == 1 or c.most_common()[1][0] == 1:
                rank = Rank.QUADS
            elif c.most_common()[2][0] == 1:
                rank = Rank.FULL_HOUSE
            else:
                rank = Rank.TWO_PAIR
        else:
            rank = Rank.QUADS if 1 in vals else Rank.TRIPS
    elif unique == 2:
        if 1 in vals:
            rank = Rank.QUINTS
        elif c.most_common()[0][1] == 3:
            rank = Rank.FULL_HOUSE
        else:
            rank = Rank.QUADS
    else:
        rank = Rank.QUINTS
    return (rank, vals)

def card_compare(a, b):
    if a[0] < b[0]:
        return -1
    if a[0] > b[0]:
        return 1
    return 1 if a[1] < b[1] else -1

def part1(hands):
    ranked = sorted(((hand_val_order(hand), bid) for hand, bid in hands),
                    key=functools.cmp_to_key(card_compare))
    return sum(i*bid for i, (_, bid) in enumerate(ranked, start=1))

def part2(hands):
    ranked = sorted(((hand_val_joker(hand), bid) for hand, bid in hands),
                    key=functools.cmp_to_key(card_compare))
    return sum(i*bid for i, (_, bid) in enumerate(ranked, start=1))

def parse_input(data_src):
    data_src.seek(0)
    hands = []
    for line in data_src.read().splitlines():
        cards, bid = line.split()
        hands.append((cards, int(bid)))
    return [hands]  # note: return single item as [item] for *parse_input

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 253205868

        assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 253907829

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (6440, 5905)
    TEST_INPUT = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
