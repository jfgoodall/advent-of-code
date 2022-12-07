#!/usr/bin/env python3
import time
from io import StringIO


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = {}
        self.dirs = {}
        self.size = 0

def print_dirs(subdir, indent=0):
    print(f"{'  '*indent}- {subdir.name} (dir: {subdir.size})")
    for name, sz in subdir.files.items():
        print(f"{'  '*(indent+1)}- {name} ({sz})")
    for d in subdir.dirs.values():
        print_dirs(d, indent+1)

def calc_dir_sizes(subdir, dir_sizes):
    size = sum(subdir.files.values())
    for d in subdir.dirs.values():
        calc_dir_sizes(d, dir_sizes)
        size += d.size
    subdir.size = size
    dir_sizes.append(size)

def part1(root):
    dir_sizes = []
    calc_dir_sizes(root, dir_sizes)
    return sum(sz for sz in dir_sizes if sz <= 100000)

def part2(root):
    dir_sizes = []
    calc_dir_sizes(root, dir_sizes)
    needed_space = 30000000 - (70000000 - root.size)
    return min(sz for sz in dir_sizes if sz >= needed_space)

def parse_input(data_src):
    data_src.seek(0)
    root = Directory('/')
    cwd = root
    for line in data_src:
        if line.startswith('$ cd'):
            directory = line.split()[-1]
            if directory == '/':
                cwd = root
            elif directory == '..':
                cwd = cwd.parent
            else:
                if not directory in cwd.dirs:
                    cwd.dirs[directory] = Directory(directory, cwd)
                cwd = cwd.dirs[directory]
        elif not line.startswith('$'):
            a, b = line.split()
            if a == 'dir':
                cwd.dirs[b] = Directory(b, cwd)
            else:
                cwd.files[b] = int(a)
    return root

def run_tests():
    TEST_INPUT = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 95437
    assert part2(parse_input(test_data)) == 24933642

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 1908462
        print_result('2', part2, parse_input(infile))  # 3979145
