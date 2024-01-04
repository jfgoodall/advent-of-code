#!/usr/bin/env python3
from enum import Enum

class OpCode(Enum):
    ACC = 'acc'
    JMP = 'jmp'
    NOP = 'nop'

def run_program(program):
    """ returns (acc, ran-to-completion) tuple """
    ip = 0  # ip = instruction pointer
    acc = 0
    counts = [0] * len(program)
    while ip < len(program) and counts[ip] == 0:
        counts[ip] += 1
        if program[ip][0] == OpCode.ACC:
            acc += program[ip][1]
            ip += 1
        elif program[ip][0] == OpCode.JMP:
            ip += program[ip][1]
        else:
            ip += 1
    return acc, ip >= len(program)

def try_swap_jmp_nop(program):
    """ swaps JMP and NOP instructions until the program runs to completion """
    for line_idx in range(len(program)):
        if program[line_idx][0] == OpCode.JMP:
            program[line_idx][0] = OpCode.NOP
            result = run_program(program)
            if result[1]:
                return result
            program[line_idx][0] = OpCode.JMP
        elif program[line_idx][0] == OpCode.NOP:
            program[line_idx][0] = OpCode.JMP
            result = run_program(program)
            if result[1]:
                return result
            program[line_idx][0] = OpCode.NOP

def parse_input(lines):
    """ creates a list of [Instuction, arg] elements """
    program = []
    for line in lines:
        tokens = line.strip().split()
        instr = OpCode(tokens[0])
        arg = int(tokens[1]) if tokens[1] else None
        program.append([instr, arg])
    return program

def test_run_program():
    test_input = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip()
    program = parse_input(test_input.split('\n'))
    assert run_program(program) == (5, False)
    assert try_swap_jmp_nop(program) == (8, True)

if __name__ == '__main__':
    test_run_program()
    with open('day08-input.dat') as infile:
        program = parse_input(infile)
    print(f"Part 1: {run_program(program)[0]}")
    print(f"Part 2: {try_swap_jmp_nop(program)[0]}")
