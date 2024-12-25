#!/usr/bin/env python3
import functools
import itertools
import time
import typing
from functools import cache
from io import StringIO


def get_bit_fn(wires, gates):
    @cache
    def get_bit(label):
        if label in wires:
            return wires[label]

        in1, in2, op = gates[label]
        in1_bit = get_bit(in1)
        in2_bit = get_bit(in2)
        match op:
            case "AND":
                return in1_bit & in2_bit
            case "OR":
                return in1_bit | in2_bit
            case "XOR":
                return in1_bit ^ in2_bit

    # create a closure so we can use @cache with unhashable
    # (but unchanging) arguments
    return get_bit

def get_number(prefix, wires, gates, bit_fn):
    number = 0
    for bit_pos in itertools.count():
        out_label = f"{prefix}{bit_pos:02}"
        if out_label in wires:
            bit = wires[out_label]
        elif out_label not in gates:
            break

        bit = bit_fn(out_label)
        number |= bit << bit_pos

    return number

def part1(wires, gates):
    bit_fn = get_bit_fn(wires, gates)
    return get_number('z', wires, gates, bit_fn)

"""
Z[n] = A[n] XOR B[n] XOR C[n]
C[0] = 0
C[n] = (A[n-1] AND B[n-1]) OR ((A[n-1] XOR B[n-1]) AND C[n-1])
Reduced cases:
  Z[0] = A[0] XOR B[0]
  Z[1] = A[1] XOR B[1] XOR (A[0] AND B[0])

z00 = x00 ^ y00
z01 = (x01 ^ y01) ^ (x00 & y00)
z02 = (x02 ^ y02) ^ (x01 & y01) | ((x01 ^ y01) & c01)

z = A ^ B ^ C
A = x_n ^ y_n
C = D | E
D = x & y
E = F & c_n-1
F = x_n-1 ^ y_n-1

XOR AND & OR are commutative and associative! ...fun...
"""

def check_carry_bit_gate(gates, c_gate, bit_pos):
    if bit_pos < 2:
        return set()

    cx, cy, cop = gates[c_gate]
    if cop != 'OR':
        return {c_gate}

    bad_gates = set()

    dx, dy, dop = gates[cx]; d = cx
    ex, ey, eop = gates[cy]; e = cy
    if {dx, dy} != {f"x{bit_pos-1:02}", f"y{bit_pos-1:02}"}:
        ex, ey, eop = gates[cx]; e = cx
        dx, dy, dop = gates[cy]; d = cy

    if dop != 'AND':
        bad_gates.add(d)
    if eop != 'AND':
        bad_gates.add(e)

    if {dx, dy} != {f"x{bit_pos-1:02}", f"y{bit_pos-1:02}"}:
        bad_gates.add(d)

    fx, fy, fop = gates[ex]; f = ex
    c_next = ey
    if fop != 'XOR':
        c_next = ex
        fx, fy, fop = gates[ey]; f = ey

    if {fx, fy} != {f"x{bit_pos-1:02}", f"y{bit_pos-1:02}"}:
        bad_gates.add(f)

    return bad_gates | check_carry_bit_gate(gates, c_next, bit_pos-1)

def check_z_gate(gates, bit_pos):
    z = f"z{bit_pos:02}"
    a, b, op = gates[z]
    bad_gates = set()

    if op != 'XOR':
        return {z}

    if bit_pos > 0:
        ax, ay, aop = gates[a]
        bx, by, bop = gates[b]

        if aop == bop:
            bad_gates.add(a)
            bad_gates.add(b)
        if aop == 'XOR' and {ax, ay} != {f"x{bit_pos:02}", f"y{bit_pos:02}"}:
            bad_gates.add(a)
        if bop == 'XOR' and {bx, by} != {f"x{bit_pos:02}", f"y{bit_pos:02}"}:
            bad_gates.add(b)

        if bit_pos == 1:
            if aop not in ('XOR', 'AND'):
                bad_gates.add(a)
            if bop not in ('XOR', 'AND'):
                bad_gates.add(b)
            if aop == 'AND' and {ax, ay} != {f"x{bit_pos-1:02}", f"y{bit_pos-1:02}"}:
                bad_gates.add(a)
            if bop == 'AND' and {bx, by} != {f"x{bit_pos-1:02}", f"y{bit_pos-1:02}"}:
                bad_gates.add(b)

    if bit_pos > 1:
        if aop not in ('XOR', 'OR'):
            bad_gates.add(a)
        if bop not in ('XOR', 'OR'):
            bad_gates.add(b)

        if aop == 'OR':
            bad_gates |= check_carry_bit_gate(gates, a, bit_pos)
        elif bop == 'OR':
            bad_gates |= check_carry_bit_gate(gates, b, bit_pos)

    return bad_gates

def part2(wires, gates):
    bit_fn = get_bit_fn(wires, gates)

    x = get_number('x', wires, gates, bit_fn)
    y = get_number('y', wires, gates, bit_fn)

    biggest_z = max(gates, key=lambda g: int(g[1:]) if g[0] == 'z' else 0)
    num_z_bits = int(biggest_z[1:]) + 1

    bad_gates = set()
    for i in range(num_z_bits):
        bad_gates |= check_z_gate(gates, i)

    # try all pairs of bad gates until one combination works
    for pairs in itertools.combinations(itertools.combinations(bad_gates, 2), 4):
        # don't know a good way to partition all possible pairs so we end up
        # with labels in multiple pairs; detect and skip
        labels = functools.reduce(lambda a, b: a | set(b), pairs, set())
        if len(labels) != 8:
            continue

        mod_gates = gates.copy()
        for a, b in pairs:
            mod_gates[a], mod_gates[b] = mod_gates[b], mod_gates[a]

        bit_fn = get_bit_fn(wires, mod_gates)
        try:
            z = get_number('z', wires, mod_gates, bit_fn)
        except RecursionError:
            # easier to catch the exception than detect circular dependencies
            continue

        if z == x + y:
            return ','.join(sorted(labels))

def parse_input(data_src: typing.TextIO) -> list[typing.Any]:
    data_src.seek(0)
    wire_lines, gate_lines = data_src.read().split('\n\n')

    wires = {}
    for wire_line in wire_lines.splitlines():
        label, value = wire_line.split(': ')
        wires[label] = int(value)

    gates = {}
    for gate_line in gate_lines.splitlines():
        in1, op, in2, _, out = gate_line.split()
        gates[out] = (in1, in2, op)

    return [wires, gates]

def main():
    (test1_data, test1_answer), (test2_data, test2_answer) = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        my_part1_answer = part1(*parse_input(test1_data))
        assert my_part1_answer == test1_answer, \
            f"got {my_part1_answer}; should be {test1_answer}"
        solve_part('1', part1, *parse_input(infile), expected=64755511006320)

        solve_part('2', part2, *parse_input(infile), expected="djg,dsd,hjm,mcq,sbg,z12,z19,z37")

def solve_part(part_label: str, part_fn: typing.Callable, *args, expected=None):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    regress = '' if expected is None or result == expected else "** Regression **"
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)  {regress}")

def get_test_data() -> tuple[tuple[str, str|float], tuple[str, str|float]]:
    """Keep test data out of the way at the bottom of this file."""
    TEST_INPUT1 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""
    TEST_ANSWER1 = 2024

    TEST_INPUT2 = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""
    TEST_ANSWER2 = "z00,z01,z02,z05"

    return (
        (StringIO(TEST_INPUT1.strip()), TEST_ANSWER1),
        (StringIO(TEST_INPUT2.strip()), TEST_ANSWER2)
    )

if __name__ == '__main__':
    main()
