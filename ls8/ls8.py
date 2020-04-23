#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
import sys

cpu = CPU()
cpu.load(sys.argv[1])  # arg[0]=ls8.py argv[1]=examples/print8.ls8.
cpu.run()
