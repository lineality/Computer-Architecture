"""CPU functionality. """

import sys


class CPU:  # OOP class: CPU
    """Main CPU class."""

    # Constructor
    def __init__(self):
        """CPU Attributes"""
        self.register = [0] * 8
        self.pc = 0  # program counter: memory address of current instruction
        self.running = True
        # instructions (individually?)
        # self.instructions = {"PRINT_BEEJ": 1, "HALT": 2, "SAVE_REG": 3, "PRINT_REG": 4}
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256  # Where does this go?

        # Internal Registers
        # PC: Program Counter, address of the currently executing instruction
        # IR: Instruction Register, contains a copy of the currently executing instruction
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        # MDR: Memory Data Register, holds the value to write or the value just read
        # FL: Flags, see below

    # Q: Where are the english instructions stored? e.g. "LDI = 0b10000010"

    #
    # LDI = 0b10000010
    # NOP = 0b00000000
    # PRN = 0b10000010
    # HLT = 0b00000001

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program is list of instruction
        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  # NOP: No operation. Do nothing for this instruction.
            0b00001000,  # this is the nubmer 8 (not an operation)
            0b01000111,  # PRN R0
            0b00000000,  # NOP: No operation. Do nothing for this instruction.
            0b00000001,  # HLT Halt
        ]

        # boiler plate
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ST(self, registerA, registerB):
        # Store value in registerB in the address stored in registerA.

        pass

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

        elif op == "XOR":
            pass

        elif op == "SHR":
            pass

        elif op == "SHL":
            pass

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.register[i], end="")

        print()

    def LDI(self, register_slot, item_immediate):
        self.register[register_slot] = item_immediate
        # codus machina:
        # 10000010 00000rrr iiiiiiii
        # 82 0r ii

    def ram_read(self, read_this_memory_slot):
        return self.ram[read_this_memory_slot]

    def ram_write(self, memory_slot, user_input):
        # 256 slots
        self.ram[memory_slot] = user_input

    # for this not to be pre-fixed
    # we'd need an input instruction list of a fixed length
    def run(self):

        self.running is True

        # load the instructions
        # self.load()

        self.pc = 0

        while self.running is True:
            # for i in range(10):
            # self.trace()

            # # test
            # for i in self.ram:
            #     print(i)

            # 0b10000010,  # LDI R0,8
            # 0b00000000,  # NOP: No operation. Do nothing for this instruction
            # 0b00001000,  # this is the nubmer 8 (not an operation)
            # 0b01000111,  # PRN R0
            # 0b00000000,  # NOP: No operation. Do nothing for this instruction
            # 0b00000001,  # HLT Halt

            # # start reading ram

            instruction = self.ram_read(self.pc)

            # instruction = memory[pc]
            # instructions are in prprint("Beej!")ograms_list
            # load data into register 08
            # print("instruction", instruction)
            # print("[self.pc]", [self.pc])

            if self.ram_read(self.pc) == 0b10000010:  # LDI
                # steps:
                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)  # bla
                # get the data
                # mask for getting self.ram[self.pc]
                operand_b = self.ram_read(self.pc + 2)

                # required to store in slot 8
                self.LDI(operand_a, operand_b)
                # self.register[operand_a] = operand_b

                # move ahead to spaces (over the data)
                # to the next self.ram[self.pc]
                self.pc += 3

                # print

            elif self.ram_read(self.pc) == 0b01000111:  # PRN
                # print register slot 8:8
                print(self.register[0])
                # move ahead one self.ram[self.pc]
                self.pc += 2
                # reg_num = memory[pc + 1]
                # value = register[reg_num]
                # print(value)
                # pc += 2

                # Halt !!
                # print("self.ram[self.pc]", self.ram_read(self.pc))
                # print("[self.pc]", [self.pc])

            elif self.ram_read(self.pc) == 0b00000001:
                print("Halt!")
                self.running = False
                break

                # print("self.ram[self.pc]", self.ram_read(self.pc))
                # print("[self.pc]", [self.pc])

            else:
                print("Unknown instruction")
                self.running = False
