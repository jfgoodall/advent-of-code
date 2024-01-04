#!/usr/bin/env python3
from collections import deque

def score(deck):
    return sum(a*b for a, b in enumerate(reversed(deck), 1))

def part1(decks):
    while all(map(len, decks)):
        a, b = decks[0].popleft(), decks[1].popleft()
        if a > b:
            decks[0].extend([a, b])
        else:
            decks[1].extend([b, a])
    winner = decks[0] if len(decks[0]) else decks[1]
    return score(winner)

def recursive_combat(deck1: tuple, deck2: tuple, return_winning_deck=False):
    previous_states = set()
    while len(deck1) and len(deck2):
        if (deck1, deck2) in previous_states:
            return 0
        previous_states.add((deck1, deck2))

        card1, card2 = deck1[0], deck2[0]
        deck1, deck2 = deck1[1:], deck2[1:]
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner_idx = recursive_combat(deck1[:card1], deck2[:card2])
        else:
            winner_idx = int(card2 > card1)

        if winner_idx == 0:
            deck1 += card1, card2
        else:
            deck2 += card2, card1

    if not return_winning_deck:
        return int(len(deck2) > 0)
    else:
        return deck1 if len(deck1) else deck2

def part2(decks):
    winner = recursive_combat(tuple(decks[0]), tuple(decks[1]), return_winning_deck=True)
    return score(winner)

def parse_input(test_input):
    decks = []
    for player in test_input.split('\n\n'):
        deck = deque(map(int, player.split('\n')[1:]))
        decks.append(deck)
    return decks

def run_tests():
    test_input = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""".strip()
    assert part1(parse_input(test_input)) == 306
    assert part2(parse_input(test_input)) == 291

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip()
    print(f"Part 1: {part1(parse_input(test_input))}")
    print(f"Part 2: {part2(parse_input(test_input))}")
