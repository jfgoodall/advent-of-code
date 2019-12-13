from enum import Enum


class IntcodeCPU:
    class _ParameterMode(Enum):
        POSITION  = 0
        IMMEDIATE = 1
        RELATIVE  = 2

    class _Instruction(Enum):
        ADD = 1
        MUL = 2
        INP = 3
        OUT = 4
        JIT = 5
        JIF = 6
        LT  = 7
        EQU = 8
        ARB = 9
        HCF = 99

    def __init__(self):
        self._instruction_map = {
            self._Instruction.ADD: self._execute_instr_ADD,
            self._Instruction.MUL: self._execute_instr_MUL,
            self._Instruction.INP: self._execute_instr_INP,
            self._Instruction.OUT: self._execute_instr_OUT,
            self._Instruction.JIT: self._execute_instr_JIT,
            self._Instruction.JIF: self._execute_instr_JIF,
            self._Instruction.LT:  self._execute_instr_LT,
            self._Instruction.EQU: self._execute_instr_EQU,
            self._Instruction.ARB: self._execute_instr_ARB,
            self._Instruction.HCF: self._execute_instr_HCF,
        }

    def _get_parameter_mode(self, param):
        return self._ParameterMode(self._get_opcode() // 10**(param+1) % 10)

    def _get_param_val_ptr(self, param):
        parameter_mode = self._get_parameter_mode(param)
        if parameter_mode == self._ParameterMode.POSITION:
            addr = self._memory[self._pc+param]
        elif parameter_mode == self._ParameterMode.IMMEDIATE:
            addr = self._pc + param
        elif parameter_mode == self._ParameterMode.RELATIVE:
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
        return self._Instruction(self._get_opcode() % 100)

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

