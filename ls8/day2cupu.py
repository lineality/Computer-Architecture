"""CPU functionality. """


class CPU:  # OOP class: CPU
    """Main CPU class."""

    # Constructor
    def __init__(self):
        """CPU Attributes"""
        self.register = [0] * 8
        self.pc = 0  # program counter: memory address of current instruction
        self.running = True
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256

        # Internal Registers
        # PC: Program Counter, address of the currently executing instruction
        # IR: Instruction Register,
        #     contains a copy of the currently executing instruction
        # MAR: Memory Address Register,
        #      holds the memory address we're reading or writing
        # MDR: Memory Data Register,
        #      holds the value to write or the value just read
        # FL: Flags, see below

    def load(self, program_filename):
        """Load a program into memory."""

        # inspection
        # print("trying to load")

        address = 0

        with open(program_filename) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()

                if line == "":
                    continue

                # set "2" for base 2
                self.ram[address] = int(line, 2)

                address += 1

        # # boiler plate
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ST(self, registerA, registerB):
        # Store value in registerB in the address stored in registerA.
        self.ram[registerA] = registerB

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa + bb

        elif op == "SUB":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa - bb

        elif op == "MUL":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa * bb

        elif op == "DIV":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa / bb

        elif op == "DIV_FlOOR":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa // bb

        elif op == "MOD":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa % bb

        elif op == "XOR":
            aa = self.register[reg_a]
            bb = self.register[reg_b]
            self.register[reg_a] = aa ^ bb

        elif op == "SHR":
            pass

        elif op == "SHL":
            pass

        else:
            raise Exception("Unsupported ALU operation")

        return self.register[reg_a]

    def trace(self):
        """
        Handy function to print out the CPU state.
        You might want to call this
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

        # argv[0] is ls8.py

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

            # # start reading ram # instruction = self.ram_read(self.pc)

            # load data into register 08
            if self.ram_read(self.pc) == 0b10000010:  # LDI

                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)  # bla
                operand_b = self.ram_read(self.pc + 2)

                # operands are like parameters
                self.LDI(operand_a, operand_b)

                # move ahead to spaces (over the data)
                # to the next self.ram[self.pc]
                self.pc += 3

            # print
            elif self.ram_read(self.pc) == 0b01000111:  # PRN
                # print register slot 8:8
                print(self.register[0])
                # move ahead one self.ram[self.pc]
                self.pc += 2

            # Halt !!
            elif self.ram_read(self.pc) == 0b00000001:
                print("Halt!")
                self.running = False
                break

            elif self.ram_read(self.pc) == 0b10100010:

                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)  # bla
                operand_b = self.ram_read(self.pc + 2)
                #
                self.alu("MUL", operand_a, operand_b)

                # move ahead to spaces (over the data)
                # to the next self.ram[self.pc]
                self.pc += 3

            else:
                print("Unknown instruction")
                self.running = False
