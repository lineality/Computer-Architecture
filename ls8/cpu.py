# ls8 emulator

# spec data
# Internal Register
# PC: Program Counter, address of the currently executing instruction
# IR: Instruction Register,
#     contains a copy of the currently executing instruction
# MAR: Memory Address Register,
#      holds the memory address we're reading or writing
# MDR: Memory Data Register,
#      holds the value to write or the value just read
# FL: Flags, see below


class CPU:  # OOP class: CPU
    """Main CPU class."""

    # optional make hash table here
    # to convert between english and instruction codes
    # static variable area:

    # Constructor (special method-function)
    def __init__(self):
        """CPU class Attributes"""
        self.register = [0] * 8
        self.pc = 0  # program counter: memory address of current instruction
        self.running = True
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256
        # see methods to push or pop stack
        # SP Stack Pointer
        # stack backward in RAM starting at F4/244
        self.SP = self.register[7] = 244

        # general method: using a hash-table
        # for matching instruction code into to functions(methods)
        # for storing (basically a hashtable)
        # faster/better than using conditionals
        self.hashtable = {}
        self.hashtable[0b10000010] = self.handle_LDI
        self.hashtable[0b00000001] = self.handle_HLT
        self.hashtable[0b10100010] = self.handle_MUL
        self.hashtable[0b01000111] = self.handle_PRN
        self.hashtable[0b01000101] = self.handle_PUSH
        self.hashtable[0b01000110] = self.handle_POP

        # alu hashtable ('hashtable')
        # before hours said this was required
        self.alu_hashtable = {}
        self.alu_hashtable["ADD"] = self.alu_ADD
        self.alu_hashtable["SUB"] = self.alu_SUB
        self.alu_hashtable["MUL"] = self.alu_MUL
        self.alu_hashtable["DIV"] = self.alu_DIV
        self.alu_hashtable["DIV_FlOOR"] = self.alu_DIV_FlOOR
        self.alu_hashtable["MOD"] = self.alu_MOD
        self.alu_hashtable["XOR"] = self.alu_XOR
        self.alu_hashtable["SHR"] = self.alu_SHR
        self.alu_hashtable["SHL"] = self.alu_SHL

    def load(self, program_filename):
        """Load a program into memory."""
        address = 0
        with open(program_filename) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
                if line == "":
                    continue
                # set "2" for "base 2"
                self.ram[address] = int(line, 2)
                address += 1

    def ST(self, registerA, registerB):
        # Store value in registerB in the address stored in registerA.
        self.ram[registerA] = registerB

    # untested
    def reg_write_plus_stack(self, reg_slot, item_to_store):
        # if the register is full, use the stack_pop
        if self.register[7] != 0:
            self.stack_push(item_to_store)
        # otherwise just store in register
        else:
            self.register[reg_slot] = item_to_store

    # alu function (method) section starts here

    def alu_ADD(self, reg_a, reg_b):  # add
        self.register[reg_a] = self.register[reg_a] + self.register[reg_b]

    def alu_SUB(self, reg_a, reg_b):  # subtract
        self.register[reg_a] = self.register[reg_a] - self.register[reg_b]

    def alu_MUL(self, reg_a, reg_b):  # multiply
        self.register[reg_a] = self.register[reg_a] * self.register[reg_b]

    def alu_DIV(self, reg_a, reg_b):  # divide
        self.register[reg_a] = self.register[reg_a] / self.register[reg_b]

    def alu_DIV_FlOOR(self, reg_a, reg_b):  # floor-divide
        self.register[reg_a] = self.register[reg_a] // self.register[reg_b]

    def alu_MOD(self, reg_a, reg_b):  # modulus/remainder
        self.register[reg_a] = self.register[reg_a] % self.register[reg_b]

    def alu_XOR(self, reg_a, reg_b):  # XOR ^
        self.register[reg_a] = self.register[reg_a] ^ self.register[reg_b]

    def alu_SHR(self, reg_a, reg_b):  # shift right >>
        self.register[reg_a] = self.register[reg_a] >> self.register[reg_b]

    def alu_SHL(self, reg_a, reg_b):  # shift left <<
        self.register[reg_a] = self.register[reg_a] << self.register[reg_b]

    # end alu section

    def alu(self, op, reg_a, reg_b):

        print("alu does: ", op)

        # uses hashtable for quick lookup of alu functions
        self.alu_hashtable[op](reg_a, reg_b)

        return self.register[reg_a]

    # boiler plate
    def trace(self):
        """
        Handy function to print out the CPU state.
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

    def ram_read(self, read_this_memory_slot):
        return self.ram[read_this_memory_slot]

    def ram_write(self, memory_slot, user_input):
        # 256 slots
        self.ram[memory_slot] = user_input

    #####
    # hashtable style methods (non-alu)
    #####

    # for understanding the operands/parameters:
    # self.ram_read(self.pc) is the current pc spot in memory
    # operand/parameter a = self.ram_read(self.pc + 1)
    # operand/parameter b = self.ram_read(self.pc + 2)

    def handle_PRN(self):
        # get operand a
        operand_a = self.ram_read(self.pc + 1)

        # operand a is the reg slot
        reg_slot = operand_a

        # perform function: print what is in that reg slot
        # TODO: ? is return and print redundant?
        return print(self.register[reg_slot])

    # Load Integer Into Register
    def handle_LDI(self):
        # stepped out for read-ability

        # make operand_a operand_b
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # a is slot, b is data
        # "immidiate" is name required in specs
        reg_slot = operand_a
        item_immediate = operand_b

        self.register[reg_slot] = item_immediate

    # Push the CPU Stack
    def handle_PUSH(self):
        # get operand a
        operand_a = self.ram_read(self.pc + 1)

        # operand a is the reg slot
        reg_slot = operand_a

        # 1. Decrement the SP.
        self.SP -= 1
        # 2. Copy value in the given register to the address pointed to by SP
        self.ram_write(self.SP, self.register[reg_slot])

    # Pop the CPU Stack
    def handle_POP(self):
        # get operand a
        operand_a = self.ram_read(self.pc + 1)

        # operand a is the reg slot
        reg_slot = operand_a

        # 1. Copy value from address pointed to by SP to the given register
        self.register[reg_slot] = self.ram_read(self.SP)
        # 2. Increment SP. increments the backwards RAM stack
        self.SP += 1

    def handle_HLT(self):
        # takes no user_input

        # what does this do? how do you stop a hash-table?
        print("You there, Halt!!")
        print("Put the peanut butter down!")
        # if using: while self.running is True
        self.running = False
        # # alternately: if using: while True
        # exit()

    # Multiply
    def handle_MUL(self):
        # make operand_a operand_b
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # call mul from alu arithmetic logic unit
        self.alu("MUL", operand_a, operand_b)

    def run(self):

        self.running is True

        while self.running is True:
            self.trace()

            # part 1 of auto advance: set length of each operation
            inst_len = ((self.ram_read(self.pc) & 0b11000000) >> 6) + 1  # 3

            # # stepped out for readability
            # # look up function in branch-table:
            # # this one-line works the same way:
            # self.hashtable[self.ram_read(self.pc)]()

            # look up function in branch-table:
            function = self.hashtable[self.ram_read(self.pc)]

            function()

            # part 2 of auto advance: set length of each operation
            self.pc += inst_len
