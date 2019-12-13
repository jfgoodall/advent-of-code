#/usr/bin/env python3
from intcode_cpu import IntcodeCPU

cpu = IntcodeCPU()

example_mem = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert cpu.run_program(example_mem) == example_mem

example_mem = [1102,34915192,34915192,7,4,7,99,0]
assert cpu.run_program(example_mem) == [1219070632396864]

example_mem = [104,1125899906842624,99]
assert cpu.run_program(example_mem) == [example_mem[1]]

with open('day9.dat') as f:
    memory = f.readlines()
    assert len(memory) == 1
    memory = list(map(int, memory[0].strip().split(',')))

output = cpu.run_program(memory, [1])
print("part 1: {}".format(output[0]))
assert output == [2436480432]

output = cpu.run_program(memory, [2])
print("part 2: {}".format(output[0]))
assert output == [45710]

