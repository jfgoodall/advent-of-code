#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

class Node:
    __slots__ = 'val', 'left', 'right'

    def __init__(self, val=None, *, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        if self.is_leaf():
            return str(self.val)
        return f'[{self.left},{self.right}]'

    def __add__(self, other):
        if not isinstance(other, Node):
            raise TypeError
        root = Node(left=self.copy(), right=other.copy())
        while explode(root) or split(root):
            pass
        return root

    def is_leaf(self):
        return self.val is not None

    def copy(self):
        if self.is_leaf():
            return Node(val=self.val)
        return Node(left=self.left.copy(), right=self.right.copy())

    def magnitude(self):
        if self.is_leaf():
            return self.val
        return 3*self.left.magnitude() + 2*self.right.magnitude()

def find_adjacent(root, target, direction) -> Node:
    found = False
    def traverse(node):
        if node is target:
            nonlocal found
            found = True
            return None
        if node.is_leaf():
            return node if found else None
        if direction == 'right':
            return traverse(node.left) or traverse(node.right)
        else:
            return traverse(node.right) or traverse(node.left)
    return traverse(root)

def explode(root, node=None, depth=0) -> bool:
    if node is None:
        node = root
    if node.is_leaf():
        return False
    if depth == 4:
        assert node.left.is_leaf() and node.right.is_leaf()
        if adj_left := find_adjacent(root, node.left, 'left'):
            adj_left.val += node.left.val
        if adj_right := find_adjacent(root, node.right, 'right'):
            adj_right.val += node.right.val
        node.left, node.right = None, None
        node.val = 0
        return True
    return explode(root, node.left, depth+1) or explode(root, node.right, depth+1)

def split(node) -> bool:
    if node.is_leaf():
        if node.val >= 10:
            node.left, node.right = Node(node.val//2), Node((node.val+1)//2)
            node.val = None
            return True
        else:
            return False
    return split(node.left) or split(node.right)

def part1(snails):
    return functools.reduce(Node.__add__, snails).magnitude()

def part2(snails):
    return max((snails[a]+snails[b]).magnitude()
               for a, b in itertools.permutations(range(len(snails)), 2))

def parse_pair(s):
    for comma in (m.start() for m in re.finditer(',', s)):
        if s[1:comma].count('[') == s[1:comma].count(']'):
            break
    children = [parse_pair(child) if child[0] == '[' else Node(int(child))
                for child in (s[1:comma], s[comma+1:-1])]
    return Node(left=children[0], right=children[1])

def parse_input(data_src):
    data_src.seek(0)
    return [parse_pair(line.strip()) for line in data_src.readlines()]

def run_tests():
    TEST_INPUT = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 4140
    assert part2(parse_input(test_data)) == 3993

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 3892
        print_result('2', part2, parse_input(infile))  # 4909
