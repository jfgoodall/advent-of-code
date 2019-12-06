from __future__ import print_function
from __future__ import division
from enum import Enum


class Instruction(Enum):
    ADD = 1
    MUL = 2
    INP = 3
    OUT = 4
    JIT = 5
    JIF = 6
    LT  = 7
    EQU = 8
    HCF = 99

    @classmethod
    def instruction_size(cls, instr):
        if   instr == cls.ADD: return 4
        elif instr == cls.MUL: return 4
        elif instr == cls.INP: return 2
        elif instr == cls.OUT: return 2
        elif instr == cls.JIT: return 3
        elif instr == cls.JIF: return 3
        elif instr == cls.LT:  return 4
        elif instr == cls.EQU: return 4
        elif instr == cls.HCF: return 1
        else: raise Exception("illegal instruction: {}".format(instr))


class IntcodeCPU(object):
    def __init__(self, memory):
        self._memory = memory
        self._pc = 0  # program counter

    def _get_parameter_mode(self, param):
        return self._get_opcode() // 10**(param+1) % 10

    def _get_param(self, param):
        parameter_mode = self._get_parameter_mode(param)
        if parameter_mode == 0:
            return self._memory[self._memory[self._pc+param]]
        elif parameter_mode == 1:
            return self._memory[self._pc+param]
        else:
            raise Exception("unknown parameter mode: {}".format(parameter_mode))

    def _set_param(self, param, val):
        parameter_mode = self._get_parameter_mode(param)
        if parameter_mode == 0:
            self._memory[self._memory[self._pc+param]] = val
        elif parameter_mode == 1:
            raise Exception("illegal parameter mode: {}".format(parameter_mode))
        else:
            raise Exception("unknown parameter mode: {}".format(parameter_mode))

    def _get_opcode(self):
        return self._memory[self._pc]

    def _get_instruction(self):
        return Instruction(self._get_opcode() % 100)

    def _advance_program_counter(self, instr):
        self._pc += Instruction.instruction_size(instr)

    def run_program(self, in_data):
        out_data = []
        while True:
            instr = self._get_instruction()
            if instr == Instruction.ADD:
                self._set_param(3, self._get_param(1) + self._get_param(2))
                self._advance_program_counter(instr)
            elif instr == Instruction.MUL:
                self._set_param(3, self._get_param(1) * self._get_param(2))
                self._advance_program_counter(instr)
            elif instr == Instruction.INP:
                self._set_param(1, in_data.pop())
                self._advance_program_counter(instr)
            elif instr == Instruction.OUT:
                out_data.append(self._get_param(1))
                self._advance_program_counter(instr)
            elif instr == Instruction.JIT:
                if self._get_param(1):
                    self._pc = self._get_param(2)
                else:
                    self._advance_program_counter(instr)
            elif instr == Instruction.JIF:
                if not self._get_param(1):
                    self._pc = self._get_param(2)
                else:
                    self._advance_program_counter(instr)
            elif instr == Instruction.LT:
                if self._get_param(1) < self._get_param(2):
                    self._set_param(3, 1)
                else:
                    self._set_param(3, 0)
                self._advance_program_counter(instr)
            elif instr == Instruction.EQU:
                if self._get_param(1) == self._get_param(2):
                    self._set_param(3, 1)
                else:
                    self._set_param(3, 0)
                self._advance_program_counter(instr)
            elif instr == Instruction.HCF:
                break
            else:
                raise Exception("illegal instruction: {}".format(instruction))

        return out_data


memory = [
    3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 2, 218, 57, 224, 101,
    -3828, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 2, 224, 1, 223, 224,
    223, 1102, 26, 25, 224, 1001, 224, -650, 224, 4, 224, 1002, 223, 8, 223,
    101, 7, 224, 224, 1, 223, 224, 223, 1102, 44, 37, 225, 1102, 51, 26, 225,
    1102, 70, 94, 225, 1002, 188, 7, 224, 1001, 224, -70, 224, 4, 224, 1002,
    223, 8, 223, 1001, 224, 1, 224, 1, 223, 224, 223, 1101, 86, 70, 225, 1101,
    80, 25, 224, 101, -105, 224, 224, 4, 224, 102, 8, 223, 223, 101, 1, 224,
    224, 1, 224, 223, 223, 101, 6, 91, 224, 1001, 224, -92, 224, 4, 224, 102,
    8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 1102, 61, 60, 225, 1001,
    139, 81, 224, 101, -142, 224, 224, 4, 224, 102, 8, 223, 223, 101, 1, 224,
    224, 1, 223, 224, 223, 102, 40, 65, 224, 1001, 224, -2800, 224, 4, 224,
    1002, 223, 8, 223, 1001, 224, 3, 224, 1, 224, 223, 223, 1102, 72, 10, 225,
    1101, 71, 21, 225, 1, 62, 192, 224, 1001, 224, -47, 224, 4, 224, 1002, 223,
    8, 223, 101, 7, 224, 224, 1, 224, 223, 223, 1101, 76, 87, 225, 4, 223, 99,
    0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227,
    247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106,
    227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274,
    1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294,
    0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225,
    225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 108, 226, 677, 224, 102,
    2, 223, 223, 1005, 224, 329, 1001, 223, 1, 223, 1107, 677, 226, 224, 102,
    2, 223, 223, 1006, 224, 344, 1001, 223, 1, 223, 7, 226, 677, 224, 1002,
    223, 2, 223, 1005, 224, 359, 101, 1, 223, 223, 1007, 226, 226, 224, 102, 2,
    223, 223, 1005, 224, 374, 101, 1, 223, 223, 108, 677, 677, 224, 102, 2,
    223, 223, 1006, 224, 389, 1001, 223, 1, 223, 107, 677, 226, 224, 102, 2,
    223, 223, 1006, 224, 404, 101, 1, 223, 223, 1108, 677, 226, 224, 102, 2,
    223, 223, 1006, 224, 419, 1001, 223, 1, 223, 1107, 677, 677, 224, 1002,
    223, 2, 223, 1006, 224, 434, 101, 1, 223, 223, 1007, 677, 677, 224, 102, 2,
    223, 223, 1006, 224, 449, 1001, 223, 1, 223, 1108, 226, 677, 224, 1002,
    223, 2, 223, 1006, 224, 464, 101, 1, 223, 223, 7, 677, 226, 224, 102, 2,
    223, 223, 1006, 224, 479, 101, 1, 223, 223, 1008, 226, 226, 224, 102, 2,
    223, 223, 1006, 224, 494, 101, 1, 223, 223, 1008, 226, 677, 224, 1002, 223,
    2, 223, 1005, 224, 509, 1001, 223, 1, 223, 1007, 677, 226, 224, 102, 2,
    223, 223, 1005, 224, 524, 1001, 223, 1, 223, 8, 226, 226, 224, 102, 2, 223,
    223, 1006, 224, 539, 101, 1, 223, 223, 1108, 226, 226, 224, 1002, 223, 2,
    223, 1006, 224, 554, 101, 1, 223, 223, 107, 226, 226, 224, 1002, 223, 2,
    223, 1005, 224, 569, 1001, 223, 1, 223, 7, 226, 226, 224, 102, 2, 223, 223,
    1005, 224, 584, 101, 1, 223, 223, 1008, 677, 677, 224, 1002, 223, 2, 223,
    1006, 224, 599, 1001, 223, 1, 223, 8, 226, 677, 224, 1002, 223, 2, 223,
    1006, 224, 614, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223,
    1006, 224, 629, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2, 223, 223,
    1005, 224, 644, 1001, 223, 1, 223, 8, 677, 226, 224, 1002, 223, 2, 223,
    1005, 224, 659, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223,
    1005, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226
]

cpu = IntcodeCPU(memory[:])
print(cpu.run_program([1]))

cpu = IntcodeCPU(memory[:])
print(cpu.run_program([5]))

