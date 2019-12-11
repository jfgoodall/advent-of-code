from __future__ import division
from enum import Enum


class IntcodeCPU(object):
    class ParameterMode(Enum):
        POSITION = 0
        IMMEDIATE = 1
        RELATIVE = 2

    def __init__(self):
        self._instruction_map = {
            1: self._execute_instr_ADD,
            2: self._execute_instr_MUL,
            3: self._execute_instr_INP,
            4: self._execute_instr_OUT,
            5: self._execute_instr_JIT,
            6: self._execute_instr_JIF,
            7: self._execute_instr_LT,
            8: self._execute_instr_EQU,
            9: self._execute_instr_ARB,
            99: self._execute_instr_HCF,
        }

    def _get_parameter_mode(self, param):
        return self.ParameterMode(self._get_opcode() // 10**(param+1) % 10)

    def _get_param_val_ptr(self, param):
        parameter_mode = self._get_parameter_mode(param)
        if parameter_mode == self.ParameterMode.POSITION:
            addr = self._memory[self._pc+param]
        elif parameter_mode == self.ParameterMode.IMMEDIATE:
            addr = self._pc + param
        elif parameter_mode == self.ParameterMode.RELATIVE:
            addr = + self._memory[self._pc+param] + self._relative_base_offset
        else:
            raise Exception("unknown parameter mode: {}".format(parameter_mode))

        assert addr >= 0
        if len(self._memory) <= addr:
            extension = addr - len(self._memory) + 1
            self._memory.extend([0]*extension)
        return addr

    def _get_param(self, param):
        addr = self._get_param_val_ptr(param)
        return self._memory[addr]

    def _set_param(self, param, val):
        addr = self._get_param_val_ptr(param)
        self._memory[addr] = val

    def _get_opcode(self):
        return self._memory[self._pc]

    def _get_instruction(self):
        return self._get_opcode() % 100

    def _advance_program_counter(self, n):
        self._pc += n

    def _execute_instr_ADD(self):
        self._set_param(3, self._get_param(1) + self._get_param(2))
        self._advance_program_counter(4)

    def _execute_instr_MUL(self):
        self._set_param(3, self._get_param(1) * self._get_param(2))
        self._advance_program_counter(4)

    def _execute_instr_INP(self):
        if self._in_data:
            self._set_param(1, self._in_data.pop(0))
            self._advance_program_counter(2)
        else:
            self._break = True

    def _execute_instr_OUT(self):
        self._out_data.append(self._get_param(1))
        self._advance_program_counter(2)

    def _execute_instr_JIT(self):
        if self._get_param(1):
            self._pc = self._get_param(2)
        else:
            self._advance_program_counter(3)

    def _execute_instr_JIF(self):
        if not self._get_param(1):
            self._pc = self._get_param(2)
        else:
            self._advance_program_counter(3)

    def _execute_instr_LT(self):
        if self._get_param(1) < self._get_param(2):
            self._set_param(3, 1)
        else:
            self._set_param(3, 0)
        self._advance_program_counter(4)

    def _execute_instr_EQU(self):
        if self._get_param(1) == self._get_param(2):
            self._set_param(3, 1)
        else:
            self._set_param(3, 0)
        self._advance_program_counter(4)

    def _execute_instr_ARB(self):
        self._relative_base_offset += self._get_param(1)
        p = self._get_param(1)
        self._advance_program_counter(2)

    def _execute_instr_HCF(self):
        self._halted = True
        self._break = True

    def _run(self, in_data, debug=False):
        assert not self.halted()
        self._break = False
        self._out_data = []
        self._in_data = list(in_data)
        while not self._break:
            if debug:
                print("inp: {}, out: {}".format(self._in_data, self._out_data))
                print("mem: {}".format(self._memory[self._pc:]))
            instr = self._get_instruction()
            self._instruction_map[instr]()

    def load_program(self, memory):
        self._pc = 0
        self._relative_base_offset = 0
        self._halted = False
        self._break = True
        self._memory = list(memory)

    def run_program(self, memory, in_data=None, debug=False):
        if in_data is None:
            in_data = []
        self.load_program(memory)
        self._run(in_data, debug=debug)
        return self._out_data

    def continue_program(self, in_data=None, debug=False):
        if in_data is None:
            in_data = []
        self._run(in_data, debug=debug)
        return self._out_data

    def halted(self):
        return self._halted

