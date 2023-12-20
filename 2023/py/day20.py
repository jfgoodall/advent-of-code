#!/usr/bin/env python3
from __future__ import annotations

import heapq
import itertools
import time
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from io import StringIO

try:
    pass
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

# sys.path.append(os.path.dirname(__file__))
# from common_patterns.point import Point2D
# from common_patterns.itertools import pairwise


Pulse = namedtuple('Pulse', ['time', 'value', 'src', 'dest'])

@dataclass
class Module:
    name: str
    type: str
    inputs: set[str]
    outputs: set[str]
    state: dict

def push_button(modules):
    def send_pulses(module, time, value):
        for dest in module.outputs:
            heapq.heappush(pulses, Pulse(pulse.time+1, value, module.name, dest))

    low_count = 0
    high_count = 0

    pulses = [Pulse(0, 0, 'button', 'broadcaster')]
    while pulses:
        pulse = heapq.heappop(pulses)
        if pulse.value:
            high_count += 1
        else:
            low_count += 1

        module = modules.get(pulse.dest, None)
        if not module:
            continue
        if module.name == 'broadcaster':
            send_pulses(module, pulse.time+1, 0)
        elif module.name == 'rx':
            module.state['value'] = pulse.value
        elif module.type == '%':
            # flip-flop
            if pulse.value == 0:
                module.state['value'] = module.state['value'] ^ 1
                send_pulses(module, pulse.time+1, module.state['value'])
        else:
            # conjunction
            module.state[pulse.src] = pulse.value
            output = int(any(v == 0 for v in module.state.values()))
            send_pulses(module, pulse.time+1, output)

    return low_count, high_count

def part1(modules):
    low, high = 0, 0
    for _ in range(1000):
        l, h = push_button(modules)
        low += l
        high += h
    return low * high


def part2(modules):
    for pushes in itertools.count(1):
        push_button(modules)
        if modules['rx'].state['value'] == 0:
            return pushes

def parse_input(data_src):
    data_src.seek(0)
    modules = {}
    for line in data_src.read().splitlines():
        mod_name, recv = line.split(' -> ')
        if mod_name[0] in '%&':
            mod_type = mod_name[0]
            mod_name = mod_name[1:]
        else:
            mod_type = ''
        modules[mod_name] = Module(mod_name, mod_type, set(), set(recv.split(', ')), defaultdict(int))

    # populate inputs
    for module in modules.values():
        for output in module.outputs:
            if output in modules:
                modules[output].inputs.add(module.name)

    # fix default values for conjunctions
    for module in modules.values():
        if module.type == '&':
            for inp in module.inputs:
                module.state[inp] = 0

    # special case for p2
    modules['rx'] = Module('rx', None, None, None, {'value': 1})

    return [modules]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # -

        # assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # -

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (11687500, 0)
    TEST_INPUT = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
    TEST_INPUT = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
    return StringIO(TEST_INPUT.strip()), TEST_RESULTS

if __name__ == '__main__':
    main()
