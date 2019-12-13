from intcode_cpu import IntcodeCPU
import itertools

def find_max_thruster_signal(memory, feedback=False):
    NUM_AMPLIFIERS = 5

    cpus = [IntcodeCPU() for _ in range(NUM_AMPLIFIERS)]
    max_signal = 0
    phase_offset = 5 if feedback else 0
    phase_range = range(0+phase_offset, NUM_AMPLIFIERS+phase_offset)
    for phases in itertools.permutations(phase_range):
        for amp in range(NUM_AMPLIFIERS):
            cpus[amp].load_program(memory)
            output = cpus[amp].continue_program([phases[amp]])
            assert not output
            assert not cpus[amp].halted()

        signal = 0
        while not cpus[0].halted():
            for amp in range(NUM_AMPLIFIERS):
                in_data = [signal]
                # print('amp: {}, starting pc: {}, in_data: {}'.format(amp, cpus[amp]._pc, in_data))
                output = cpus[amp].continue_program(in_data)
                # print('break: {}, halted: {}, output: {}'.format(
                #     cpus[amp]._break, cpus[amp].halted(), output))
                signal = output[0]
                # print('breaking pc: {}, signal: {}, max_signal: {}'.format(
                #     cpus[amp]._pc, signal, max_signal))
            max_signal = max(max_signal, signal)
        assert all([cpu.halted() for cpu in cpus])
    return max_signal


example_mem = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert find_max_thruster_signal(example_mem) == 43210

example_mem = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,
               23,99,0,0]
assert find_max_thruster_signal(example_mem) == 54321

example_mem = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,
               1,33,31,31,1,32,31,31,4,31,99,0,0,0]
assert find_max_thruster_signal(example_mem) == 65210

memory = [
    3,8,1001,8,10,8,105,1,0,0,21,34,51,76,101,126,207,288,369,450,99999,3,9,
    102,4,9,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,
    102,5,9,9,1001,9,2,9,102,2,9,9,101,3,9,9,1002,9,2,9,4,9,99,3,9,101,5,9,9,
    102,5,9,9,1001,9,2,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,1002,9,5,9,
    1001,9,5,9,1002,9,4,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,
    9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,
    9,3,9,1001,9,2,9,4,9,3,9, 1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,
    4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,
    9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,
    9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,
    9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,
    4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,
    4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,
    9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,
    4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,
    9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,
    9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,
    4,9,99
]
signal = find_max_thruster_signal(memory)
print("part 1: {}".format(signal))
assert signal == 422858

example_mem = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,
               28,1005,28,6,99,0,0,5]
assert find_max_thruster_signal(example_mem, feedback=True) == 139629729

example_mem = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,
               54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,
               53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
assert find_max_thruster_signal(example_mem, feedback=True) == 18216

signal = find_max_thruster_signal(memory, feedback=True)
print("part 2: {}".format(signal))
assert signal == 14897241

