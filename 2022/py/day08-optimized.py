#!/usr/bin/env python3
"""
Import-free solutions with redundant parsing and test execution removed for
faster overall script execution (to make comparison tests fair).

End-to-end script execution, including environment startup, library imports,
file I/O, and test execution (median /usr/bin/time value over several runs):
         Original             Optimized
         real    0m0.393s     real    0m0.047s
         user    0m0.314s     user    0m0.024s
         sys     0m0.217s     sys     0m0.005s

Using time.perf_counter to compare algorithm performance, ignoring environment
startup overhead and file I/O (averaged over several runs):
         Original  Optimized
          135 ms     1 ms     Part 1
           42 ms     9 ms     Part 2
"""

def part1(trees):
    rows, cols = len(trees), len(trees[0])
    visible = [0] * cols * rows

    # views from left and top
    left_view = [row[0] for row in trees]
    top_view = list(trees[0])
    for i in range(1, rows-1):
        row = trees[i]
        for j in range(1, cols-1):
            height = row[j]
            if height > left_view[i]:
                left_view[i] = height
                visible[i*cols+j] = 1
            if height > top_view[j]:
                top_view[j] = height
                visible[i*cols+j] = 1

    # views from right and bottom
    right_view = [row[-1] for row in trees]
    bottom_view = list(trees[-1])
    for i in range(rows-2, 0, -1):
        row = trees[i]
        for j in range(cols-2, 0, -1):
            height = row[j]
            if height > right_view[i]:
                right_view[i] = height
                visible[i*cols+j] = 1
            if height > bottom_view[j]:
                bottom_view[j] = height
                visible[i*cols+j] = 1

    return sum(visible) + rows*2 + cols*2 - 4

def part2(trees):
    rows, cols = len(trees), len(trees[0])
    max_score = 0
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            height = trees[i][j]

            left = j - 1
            while left > 0 and height > trees[i][left]:
                left -= 1

            right = j + 1
            while right < cols-1 and height > trees[i][right]:
                right += 1

            up = i - 1
            while up > 0 and height > trees[up][j]:
                up -= 1

            down = i + 1
            while down < rows-1 and height > trees[down][j]:
                down += 1

            score = (j-right) * (left-j) * (i-up) * (down-i)
            if score > max_score:
                max_score = score

    return max_score

if __name__ == '__main__':
    # import time
    with open('day08-input.dat') as infile:
        trees = infile.read().splitlines()

        # start = time.perf_counter()
        result = part1(trees)
        # end = time.perf_counter()
        # print(int((end-start)*1000), 'ms: ', end='')
        print(result)

        # start = time.perf_counter()
        result = part2(trees)
        # end = time.perf_counter()
        # print(int((end-start)*1000), 'ms: ', end='')
        print(result)
