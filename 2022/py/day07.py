#!/usr/bin/env python3
import time
from io import StringIO


class Directory:
    def __init__(self, parent=None):
        self._parent: Final[Directory] = parent
        self.subdirs: dict[str, Directory] = {}
        self.files: list[int] = []  # just file sizes; names don't matter

    def mkdir(self, dirname):
        if not dirname in self.subdirs:
            self.subdirs[dirname] = Directory(parent=self)
        return self.subdirs[dirname]

    def chdir(self, dirname, root):
        if dirname == '/':
            return root
        elif dirname == '..':
            return self._parent
        return self.mkdir(dirname)

    def calc_dir_sizes(self) -> [int]:
        """Return list of sizes of contained subdirectories. Last element
        contains the total size of self.
        """
        self_size = sum(self.files)
        dir_sizes = []
        for subdir in self.subdirs.values():
            dir_sizes += subdir.calc_dir_sizes()
            self_size += dir_sizes[-1]
        dir_sizes.append(self_size)
        return dir_sizes

def print_dirs(directory, dirname='/', indent=0):
    print(f"{'  '*indent}- dir: {dirname}")
    for sz in directory.files:
        print(f"{'  '*(indent+1)}- file: {sz}")
    for dirname, subdir in directory.subdirs.items():
        print_dirs(subdir, dirname, indent+1)

def part1(root):
    MAX_DIR_SIZE = 100000

    dir_sizes = root.calc_dir_sizes()
    return sum(sz for sz in dir_sizes if sz <= MAX_DIR_SIZE )

def part2(root):
    TOTAL_DISK_SPACE = 70000000
    REQUIRED_UNUSED_SPACE = 30000000

    dir_sizes = root.calc_dir_sizes()
    min_dir_size = REQUIRED_UNUSED_SPACE - (TOTAL_DISK_SPACE - dir_sizes[-1])
    return min(sz for sz in dir_sizes if sz >= min_dir_size)

def parse_input(data_src):
    data_src.seek(0)
    root = Directory()
    cwd = root
    for line in data_src:
        if line.startswith('$ cd'):
            cwd = cwd.chdir(line.split()[-1], root)
        elif not line.startswith('$'):
            sz, _ = line.split()
            if sz != 'dir':
                cwd.files.append(int(sz))
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
