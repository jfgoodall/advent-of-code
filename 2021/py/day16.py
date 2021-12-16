#!/usr/bin/env python3
import time, itertools, functools
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def parse_ver(bits, idx):
    ver = int(bits[idx:idx+3], 2)
    typ = int(bits[idx+3:idx+6], 2)
    idx += 6
    if typ == 4:  # literal
        while True:
            idx += 5
            if bits[idx-5] == '0':
                break
    else:
        length_id = bits[idx]
        idx += 1
        if length_id == '0':
            sub_bits = int(bits[idx:idx+15], 2)
            idx += 15
            end_idx = idx + sub_bits
            while idx != end_idx:
                assert idx < end_idx
                idx, v2 = parse_ver(bits, idx)
                ver += v2
        else:
            sub_packets = int(bits[idx:idx+11], 2)
            idx += 11
            for _ in range(sub_packets):
                idx, v2 = parse_ver(bits, idx)
                ver += v2
    return idx, ver

def part1(bits):
    return parse_ver(bits, 0)[1]

def parse_val(bits, idx):
    ver = int(bits[idx:idx+3], 2)
    typ = int(bits[idx+3:idx+6], 2)
    idx += 6
    if typ == 4:  # literal
        val = ''
        while True:
            val += bits[idx+1:idx+5]
            idx += 5
            if bits[idx-5] == '0':
                break
        val = int(val, 2)
    else:
        length_id = bits[idx]
        idx += 1
        vals = []
        if length_id == '0':
            sub_bits = int(bits[idx:idx+15], 2)
            assert idx + sub_bits <= len(bits)
            idx += 15
            end_idx = idx + sub_bits
            while idx != end_idx:
                assert idx < end_idx
                idx, val = parse_val(bits, idx)
                vals.append(val)
        else:
            sub_packets = int(bits[idx:idx+11], 2)
            idx += 11
            for _ in range(sub_packets):
                idx, val = parse_val(bits, idx)
                vals.append(val)

        if typ == 0:  # sum
            val = sum(vals)
        elif typ == 1:  # product
            val = np.product(vals)
        elif typ == 2:  # minimum
            val = min(vals)
        elif typ == 3:  # maximum
            val = max(vals)
        elif typ == 5:  # greater than
            assert len(vals) == 2
            val = int(vals[0] > vals[1])
        elif typ == 6:  # less than
            assert len(vals) == 2
            val = int(vals[0] < vals[1])
        elif typ == 7:  # equal to
            assert len(vals) == 2
            val = int(vals[0] == vals[1])
        else:
            assert False
    return idx, val

def part2(bits):
    return parse_val(bits, 0)[1]

def parse_input(data_src):
    data_src.seek(0)
    return ''.join(f'{int(x,16):04b}' for x in next(data_src).strip())

def run_tests():
    assert part1(parse_input(StringIO('D2FE28'))) == 6
    assert part1(parse_input(StringIO('38006F45291200'))) == 9
    assert part1(parse_input(StringIO('EE00D40C823060'))) == 14
    assert part2(parse_input(StringIO('D2FE28'))) == 2021
    assert part2(parse_input(StringIO('C200B40A82'))) == 3
    assert part2(parse_input(StringIO('04005AC33890'))) == 54
    assert part2(parse_input(StringIO('9C0141080250320F1802104A08'))) == 1

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        print_result('1', part1, parse_input(infile))  # 984
        print_result('2', part2, parse_input(infile))  # 1015320896946
