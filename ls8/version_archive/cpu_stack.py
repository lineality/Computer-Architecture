"""CPU functionality. """
# currenlty this requres another file ls8.py to run, which also loads program
# run from terminal with line such as:
# $ python3 ls8.py examples/sctest.ls8

# Q: Alphabetical order for methods?


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
        # see methods to push or pop stack
        # SP Stack Pointer
        # self.stack_pointer = 244  # stack backward in RAM starting at F4/244
        self.SP = self.register[7] = 244
        self.branchtable = {}

    def load(self, program_filename):  # loads any external ls8 program file
        """Load a program into memory."""

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

    def ST(self, registerA, registerB):
        # Store value in registerB in the address stored in registerA.
        self.ram[registerA] = registerB

    # untested, experimental (automatically use stack if reg full)
    def reg_write_plus_stack(self, reg_slot, item_to_store):
        # if the register is full, use the stack_pop
        if self.register[7] != 0:
            self.stack_push(item_to_store)
        # otherwise just store in register
        else:
            self.register[reg_slot] = item_to_store

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
        # loads immidate (direct value, not pointer) into a register
        self.register[register_slot] = item_immediate

    def prints(self, reg_slot):
        # prints contents of register slot
        return print(self.register[reg_slot])

    def ram_read(self, read_this_memory_slot):
        # reads ram
        return self.ram[read_this_memory_slot]

    def ram_write(self, memory_slot, user_input):
        # writes to ram: 256 slots FF is end
        self.ram[memory_slot] = user_input

    def stack_push(self, reg_slot):
        # 1. Decrement the SP.
        self.SP -= 1
        # 2. Copy value in the given register to the address pointed to by SP.
        self.ram_write(self.SP, self.register[reg_slot])

    def stack_pop(self, reg_slot):
        # 1. Copy value from address pointed to by SP to the given register.
        # return to reg item that was at top of the backwards stack
        self.register[reg_slot] = self.ram_read(self.SP)
        # 2. Increment SP.
        # increments the backwards RAM stack
        self.SP += 1

    # comments from assignment:
    # for this not to be pre-fixed
    # we'd need an input instruction list of a fixed length
    def run(self):

        # argv[0] is ls8.py

        self.running is True

        ##############
        # While Loop #
        ##############

        # load the instructions  (this is currently done with external file)
        # self.load()

        self.pc = 0

        while self.running is True:  # iterate through loaded program
            # # start reading ram # instruction = self.ram_read(self.pc)

            # for i in range(10):
            self.trace()

            # set length of each operation
            inst_len = ((self.ram_read(self.pc) & 0b11000000) >> 6) + 1  # 3

            # load data into register 08
            if self.ram_read(self.pc) == 0b10000010:  # LDI

                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)  # bla
                operand_b = self.ram_read(self.pc + 2)

                # operands are like parameters
                self.LDI(operand_a, operand_b)

            elif self.ram_read(self.pc) == 0b01000111:  # PRN
                # make operand_a
                operand_a = self.ram_read(self.pc + 1)  # bla

                # print register slot 8:8
                self.prints(operand_a)

            # Halt !!
            elif self.ram_read(self.pc) == 0b00000001:
                print("Halt!")
                self.running = False
                break

            # MUL
            elif self.ram_read(self.pc) == 0b10100010:

                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)  # bla
                operand_b = self.ram_read(self.pc + 2)
                #
                self.alu("MUL", operand_a, operand_b)

            # PUSH (stack)
            elif self.ram_read(self.pc) == 0b01000101:

                # operand_a is the Register memory slot
                operand_a = self.ram_read(self.pc + 1)
                self.stack_push(operand_a)

            # POP (stack)
            elif self.ram_read(self.pc) == 0b01000110:

                # make operand_a operand_b
                operand_a = self.ram_read(self.pc + 1)
                self.stack_pop(operand_a)

            else:
                print("Unknown instruction")
                self.running = False

            self.pc += inst_len
