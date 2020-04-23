"""CPU functionality. """

import sys

class CPU:  # OOP class: CPU 
    """Main CPU class."""

    # Constructor
    def __init__(self):
        """CPU Attributes"""
        self.register = [0] * 8
        self.memory = []
        self.pc = 0  # program counter: memory address of current instruction
        self.running = True
        # instructions (individually?)
        self.instructions = {PRINT_BEEJ: 1, HALT: 2, SAVE_REG: 3, PRINT_REG: 4}
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256  # Where does this go?

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program is list of instruction
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # NOP: No operation. Do nothing for this instruction.
            0b00001000,
            0b01000111, # PRN R0
            0b00000000, # NOP: No operation. Do nothing for this instruction.
            0b00000001, # HLT Halt
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "DIV_FlOOR":
            self.reg[reg_a] //= self.reg[reg_b]

        elif op == "MOD":
            self.reg[reg_a] % self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, read_this_memory_slot):
        self.ram[read_this_memory_slot]

    def ram_write(self, memory_slot, user_input):
        # 256 slots
        self.ram[memory_slot] = user_input

    # for this not to be pre-fixed
    # we'd need an input instruction list of a fixed length
    def run(self):
        self.running == True

        while self.running:
            #instruction = memory[pc]
            # instructions are in programs_list

            if instruction[0]: #== PRINT_BEEJ:
                # print("Beej!")
                # pc += 1

            elif instruction[1] # == SAVE_REG:
                # reg_num = memory[pc + 1]
                # value = memory[pc + 2]
                # register[reg_num] = value
                # pc += 3

            elif instruction[2]:
                # reg_num = memory[pc + 1]
                # value = register[reg_num]
                # print(value)
                # pc += 2

            elif instruction[3]:
                # reg_num = memory[pc + 1]
                # value = register[reg_num]
                # print(value)
                # pc += 2

            else:
                print("Unknown instruction")
                self.running = False
