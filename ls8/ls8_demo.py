#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()


memory = [
	PRINT_BEEJ,

	SAVE_REG,    # SAVE R0,37   store 37 in R0      the opcode
	0,  # R0     operand ("argument")
	37, # 37     operand

	PRINT_BEEJ,

	PRINT_REG,  # PRINT_REG R0
	0, # R0

	HALT
]

# what is this called?
# loop through memory, and run the things
while running:
	inst = memory[pc]

	if inst == PRINT_BEEJ:
		print("Beej!")
		pc += 1

	elif inst == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif inst == PRINT_REG:
		reg_num = memory[pc + 1]
		value = register[reg_num]
		print(value)
		pc += 2

	elif inst == HALT:
		running = False

	else:
		print("Unknown instruction")
		running = False