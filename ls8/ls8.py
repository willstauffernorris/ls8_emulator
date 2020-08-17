#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()

## Checking out what's in the RAM
print(cpu.ram)
print(cpu.ram_read(0))

cpu.ram_write("overwritten!", 0)

print(cpu.ram_read(0))