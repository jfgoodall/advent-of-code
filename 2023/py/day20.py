#!/usr/bin/env python3
import itertools
import time
from collections import deque, namedtuple
from dataclasses import dataclass
from io import StringIO

import numpy as np

Pulse = namedtuple('Pulse', ['value', 'src', 'dest'])
STARTING_PULSE = Pulse(0, 'button', 'broadcaster')

@dataclass
class Module:
    name: str
    type: str
    inputs: set[str]
    outputs: set[str]
    state: dict

def send_pulses(module, value, pulse_train):
    for dest in module.outputs:
        pulse_train.append(Pulse(value, module.name, dest))

def apply_next_pulse(pulse_train, modules):
    pulse = pulse_train.popleft()
    if module := modules.get(pulse.dest):
        if module.type == '%':
            # flip-flop
            if pulse.value == 0:
                module.state['value'] ^= 1
                send_pulses(module, module.state['value'], pulse_train)
        elif module.type == '&':
            # conjunction
            module.state[pulse.src] = pulse.value
            output = int(any(v == 0 for v in module.state.values()))
            send_pulses(module, output, pulse_train)
        elif module.name == 'broadcaster':
            send_pulses(module, 0, pulse_train)
    return pulse

def part1(modules):
    pulse_count = 0
    pulse_sum = 0
    for _ in range(1000):
        pulse_train = deque([STARTING_PULSE])
        while pulse_train:
            pulse = apply_next_pulse(pulse_train, modules)
            pulse_count += 1
            pulse_sum += pulse.value
    return pulse_sum * (pulse_count-pulse_sum)

def part2(modules):
    # find the module outputting to rx
    for module in modules.values():
        if 'rx' in module.outputs:
            key_module = module
            break
    key_inputs = {}

    for pushes in itertools.count(1):
        pulse_train = deque([STARTING_PULSE])
        while pulse_train:
            pulse = apply_next_pulse(pulse_train, modules)

            # record the number of pushes required to turn on a key input we haven't seen yet
            if (pulse.dest == key_module.name and
                pulse.src not in key_inputs and
                pulse.value == 1
            ):
                key_inputs[pulse.src] = pushes

        # quit searching when all key inputs have a cycle count
        if len(key_inputs) == len(key_module.inputs):
            break

    # how many pushes for all key inputs to turn on
    return np.lcm.reduce(list(key_inputs.values()))

def parse_input(data_src):
    data_src.seek(0)
    modules = {}
    for line in data_src.read().splitlines():
        mod_name, recv = line.split(' -> ')
        mod_type = ''
        mod_state = None
        if mod_name[0] == '%':
            mod_type = mod_name[0]
            mod_name = mod_name[1:]
            mod_state = {'value': 0}
        elif mod_name[0] in '&':
            mod_type = mod_name[0]
            mod_name = mod_name[1:]
            mod_state = {}
        modules[mod_name] = Module(mod_name, mod_type, set(),
                                   set(recv.split(', ')), mod_state)

    # populate inputs
    for module in modules.values():
        for output in module.outputs:
            if m := modules.get(output):
                m.inputs.add(module.name)

    # fix default values for conjunctions
    for module in modules.values():
        if module.type == '&':
            for inp in module.inputs:
                module.state[inp] = 0

    return [modules]

def main():
    test_data, test_answers = get_test_data()
    with open(__file__[:-3] + '-input.dat') as infile:
        assert part1(*parse_input(test_data)) == test_answers[0]
        print_result('1', part1, *parse_input(infile))  # 703315117

        # assert part2(*parse_input(test_data)) == test_answers[1]
        print_result('2', part2, *parse_input(infile))  # 230402300925361

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

def get_test_data():
    """Keep test data out of the way at the bottom of this file."""
    TEST_RESULTS = (11687500, 0)
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
