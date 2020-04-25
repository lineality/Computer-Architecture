# ls8 emulator in python, loading files in examples folder(directory)
# currenlty this requres another file ls8.py to run, which also loads program
# run from terminal with line such as:
# $ python3 ls8.py examples/sctest.ls8


class CPU:  # OOP class: CPU
    """Main CPU class."""

    # optional: make hash table here
    # e.g. to convert between english and instruction codes
    # static variable area:

    # Constructor (special method-function)
    def __init__(self):
        """CPU class Attributes"""
        self.register = [0] * 8
        self.pc = 0  # program counter: memory address of current instruction
        self.fl = 0  # flag register special
        # 3 equality flags E,L,G
        self.E = 0  # = "equal flag", True=1, False=0
        self.L = 0  # < less than flag, True=1, False=0
        self.G = 0  # > greater than flag, True=1, False=0
        self.running = True
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256
        # see methods to push or pop stack
        # SP Stack Pointer
        # stack backward in RAM starting at F4/244
        self.SP = self.register[7] = 244

        # general method: using a branch-table/jumptable (a dictionary!)
        # for matching instruction code into to functions(methods)
        # for storing (basically a jumptable)
        # faster/better than using conditionals
        self.jumptable = {}
        self.jumptable[0b10000010] = self.handle_LDI  # load into register
        self.jumptable[0b00000001] = self.handle_HLT  # halt, stop
        self.jumptable[0b10100000] = self.handle_ADD  # add (alu)
        self.jumptable[0b10100010] = self.handle_MUL  # multiply (alu)
        self.jumptable[0b01000111] = self.handle_PRN  # Print
        self.jumptable[0b01000101] = self.handle_PUSH  # push to stack
        self.jumptable[0b01000110] = self.handle_POP  # pop stack
        self.jumptable[0b01010000] = self.handle_CALL  # call and return
        self.jumptable[0b00010001] = self.handle_RET  # call and return
        #
        # Sprint Challenge:
        self.jumptable[0b01010100] = self.handle_JMP  # jump to register
        # cmp: Compare values in two registers
        self.jumptable[0b10100111] = self.handle_CMP  # cmp
        self.jumptable[0b01010110] = self.handle_JNE  # JNE
        # JEQ: Jump if Equal (check E flag)
        self.jumptable[0b01010101] = self.handle_JEQ  # JEQ

        # alu jumptable ('jumptable')
        # before hours said this was required
        self.alu_jumptable = {}
        self.alu_jumptable["ADD"] = self.alu_ADD
        self.alu_jumptable["SUB"] = self.alu_SUB
        self.alu_jumptable["MUL"] = self.alu_MUL
        self.alu_jumptable["DIV"] = self.alu_DIV
        self.alu_jumptable["DIV_FlOOR"] = self.alu_DIV_FlOOR
        self.alu_jumptable["MOD"] = self.alu_MOD
        self.alu_jumptable["XOR"] = self.alu_XOR
        self.alu_jumptable["SHR"] = self.alu_SHR
        self.alu_jumptable["SHL"] = self.alu_SHL

    #####
    # jumptable style methods (non-alu)
    #####

    # for understanding the operands/parameters:
    # self.ram_read(self.pc) is the current pc spot in memory
    # operand/parameter a = self.ram_read(self.pc + 1)
    # operand/parameter b = self.ram_read(self.pc + 2)

    # alu itself
    def alu(self, op, reg_a, reg_b):
        # inspection
        # print("alu does: ", op)

        # uses jumptable for quick lookup of alu functions
        self.alu_jumptable[op](reg_a, reg_b)
        return self.register[reg_a]

    # Add
    def handle_ADD(self):
        # inspection
        # print("adding...")

        # make operand_a operand_b
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # call mul from alu arithmetic logic unit
        self.alu("ADD", operand_a, operand_b)

    def handle_CMP(self):
        # this works with 3 register flags: E, L, G
        # compare values in 2 registers
        # not the values listed after in immidiate instructions,
        # but rather the values those point to in Register:

        reg_a_value = self.register[self.ram_read(self.pc + 1)]
        reg_b_value = self.register[self.ram_read(self.pc + 2)]

        # inspection:
        # print(f"CMP: {reg_a_value} vs {reg_b_value}")

        # = If they are equal,
        # set the Equal E flag to 1, otherwise set it to 0.
        if reg_a_value == reg_b_value:
            self.E = 1

        else:  # reg_a_value != reg_b_value:
            self.E = 0

        # < If registerA is less than registerB,
        # set the Less-than L flag to 1, otherwise set it to 0.
        if reg_a_value < reg_b_value:
            self.L = 1

        else:  # reg_a_value !< reg_b_value:
            self.L = 0

        # > If registerA is greater than registerB,
        # set the Greater-than G flag to 1, otherwise set it to 0.
        if reg_a_value > reg_b_value:
            self.G = 1

        else:  # reg_a !> reg_b:
            self.G = 0

        # insepction
        # print(f"E: {self.E}, L: {self.L}, G: {self.G}")

    # Multiply
    def handle_MUL(self):
        # inspection
        # print("multiplying...")

        # make operand_a operand_b
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # call mul from alu arithmetic logic unit
        self.alu("MUL", operand_a, operand_b)

    ##########
    #  for ALU
    ##########

    # alu_jumptable functions (methods) section starts here

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

    def handle_HLT(self):
        # takes no user_inputLDI

        # what does this do? how do you stop a hash-table?
        print("You there, Halt!!")
        print("Put the peanut butter down!")
        # if using: while self.running is True
        self.running = False
        # # alternately: if using: while True
        # exit()

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

    # Load Integer Into Register
    def handle_LDI(self):

        # make operand_a operand_b
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # # inpection
        # print("Hands up! This is the LDI!")
        # print("reg_slot = operand_a: ", operand_a)
        # print("item_immediate = operand_b: ", operand_b)

        # a is slot, b is data
        # "immidiate" is name required in specs
        reg_slot = operand_a
        item_immediate = operand_b
        # print("item_immediate", item_immediate)

        self.register[reg_slot] = item_immediate

    # Load Integer Into Register
    def handle_JEQ(self):
        # this is similar to JMP,
        # BUT it only jumps if E-flag is True

        if self.E == 1:
            # this is similar to call-return, but just jumps

            # set the program_counter to the number in reg from previous LDI
            self.pc = self.register[self.ram_read(self.pc + 1)]

            # TODO: maybe move the stack back one just in case?
            self.pc -= 2

    # Load Integer Into Register
    def handle_JMP(self):
        # this is similar to call-return, but just jumps

        # set the program_counter to the number in reg from previous LDI
        self.pc = self.register[self.ram_read(self.pc + 1)]

        # TODO: maybe move the stack back one just in case?
        self.pc -= 2

    # Load Integer Into Register
    def handle_JNE(self):
        # this is similar to JEQ,
        # BUT it only jumps if E-flag is False

        if self.E == 0:
            # this is similar to call-return, but just jumps

            # set the program_counter to the number in reg from previous LDI
            self.pc = self.register[self.ram_read(self.pc + 1)]

            # TODO: maybe move the stack back one just in case?
            self.pc -= 2

    # Push the CPU Stack
    def handle_PUSH(self):
        # print("push is happening...happening...")

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

    # print
    def handle_PRN(self):
        # get operand a
        operand_a = self.ram_read(self.pc + 1)

        # inspection
        # print("printing reg slot: ", operand_a)

        # operand a is the reg slot
        reg_slot = operand_a

        # perform function: print what is in that reg slot
        # TODO: ? is return and print redundant?
        return print(self.register[reg_slot])

    # Call Register
    # (for call and return)
    def handle_CALL(self):  # 1 operand/parameter: the next pc
        # print("Who you call now?")
        # handle_CALL stores (stack push) the address "afterwards"
        # to return to later...but
        # this isn't standard operand_a = self.ram_read(self.pc + 1)
        # it's "self.pc + 2", the location itself the one after that!

        # Step 1: Push
        # So do a modified push: reaching out 2 spaces
        # modified read...binary...

        # get operand a
        operand_a = self.pc + 2

        # 1. Decrement the SP.
        self.SP -= 1
        # 2. Copy value in the given register to the address pointed to by SP
        self.ram_write(self.SP, operand_a)

        # Step 2:
        # set the program_counter to the number in reg from previous LDI
        self.pc = self.register[self.ram_read(self.pc + 1)]

        # TODO: maybe move the stack back one just in case?
        self.pc -= 2

    # Return (to PC operation stored at top of stack)
    # (for call and return)
    def handle_RET(self):
        # ...no instruction for whttps://tetrix.now.sh/here to pop to
        # So: do a modified POP, move directly to: self.pc = that

        # 1. Copy value from address pointed to by SP to the given register
        self.pc = self.ram_read(self.SP)
        # 2. Increment SP. increments the backwards RAM stack
        self.SP += 1

        # move the stack back one to offset auto advance
        self.pc -= 1

    def ST(self, registerA, registerB):
        # Store value in registerB in the address stored in registerA.
        self.ram[registerA] = registerB

    # boiler plate: so ugly...
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

    # read (RAM)
    def ram_read(self, read_this_memory_slot):
        return self.ram[read_this_memory_slot]

    # write (RAM)
    def ram_write(self, memory_slot, user_input):
        # 256 slots
        self.ram[memory_slot] = user_input

    # untested: experimental auto use of stack...
    def reg_write_plus_stack(self, reg_slot, item_to_store):
        # if the register is full, use the stack_pop
        if self.register[7] != 0:
            self.stack_push(item_to_store)
        else:  # otherwise just store in register
            self.register[reg_slot] = item_to_store

    # Call
    def run(self):

        self.running is True

        while self.running is True:  # alternately, while True, then exit()
            # #  optional: prints trace
            # self.trace()

            # Auto-Advance Program-Counter 1:2
            # part 1 of auto advance: set length of each operation
            inst_len = ((self.ram_read(self.pc) & 0b11000000) >> 6) + 1  # 3

            # # Regarding the next 2 lines of code:
            # # They stepped out for readability:
            # # 1. look up function in branch-table.
            # #    that is, the function the PC counter points to.
            # # 2. Run that function
            # # this one-line works the same way:
            # self.jumptable[self.ram_read(self.pc)]()

            # 1. look up function in branch-table:
            function = self.jumptable[self.ram_read(self.pc)]
            # 2. call that function
            function()

            # Auto-Advance Program-Counter 2:2
            # part 2 of auto advance: set length of each operation
            self.pc += inst_len
