#!/usr/bin/env python3

def apply_mask1(mask, val):
    result = 0
    result_mask = 1 << 35
    for bit in mask:
        if bit == 'X':
            result |= result_mask & val
        elif bit == '1':
            result |= result_mask
        else:
            result &= ~result_mask
        result_mask >>= 1
    return result

def part1(instructions):
    mem = {}
    for instr in instructions:
        if len(instr) == 36:
            mask = instr
        else:
            idx, val = instr
            mem[idx] = apply_mask1(mask, val)
    return sum(mem.values())

def apply_mask2(mask, val):
    from itertools import product
    results = []
    for perm in product(('_', '1'), repeat=mask.count('X')):
        perm_iter = iter(perm)
        result_mask = 1 << 35
        result = val
        for bit in mask:
            bit = bit if bit != 'X' else next(perm_iter)
            if bit == '0':
                result |= result_mask & val
            elif bit == '1':
                result |= result_mask
            else:
                result &= ~result_mask
            result_mask >>= 1
        results.append(result)
    return results

def part2(instructions):
    mem = {}
    for instr in instructions:
        if len(instr) == 36:
            mask = instr
        else:
            idx, val = instr
            for i in apply_mask2(mask, idx):
                mem[i] = val
    return sum(mem.values())

def parse_input(lines):
    import re
    mask_re = re.compile(r'^mask = ([X01]{36})$')
    instr_re = re.compile(r'^mem\[(\d+)] = (\d+)$')
    instructions = []
    for line in lines:
        match = mask_re.match(line)
        if match:
            instructions.append(match.groups()[0])
        else:
            instructions.append(tuple(map(int, instr_re.match(line).groups())))
    return instructions

def run_tests():
    test_input = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().split('\n')
    instructions = parse_input(test_input)
    assert part1(instructions) == 165

    test_input = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().split('\n')
    instructions = parse_input(test_input)
    assert part2(instructions) == 208

if __name__ == '__main__':
    run_tests()
    with open('day14-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    instructions = parse_input(test_input)
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")
