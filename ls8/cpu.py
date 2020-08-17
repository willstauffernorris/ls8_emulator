"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        # Program counter
        # PC stores the address of the currently executing instruction
        # the index into the array of the currently executing instruction
        self.PC = [0]
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        #starts at 0
        self.PC = 0



        operand_a = self.ram_read(self.PC+1)
        operand_b = self.ram_read(self.PC+2)

        # dpending on the value of the opcode
        # perform the actions needed for the instruction
        while self.PC < 8:

            #instruction register
            IR = self.ram[self.PC]

            #if ...._

            #elif ......

            #else ....

            #if HLT:
            if IR == 0b00000001:
                print("IR!!!")
                exit()

            elif IR == 130:
                #Set the value of a register to an integer.
                print("INT")

            elif IR == 0b01000111:
                print("PRN")

            

            print(IR)
            print(type(IR))

            print(IR == 130)



            # somehow this doesn't work


            #elif LDI\
            #`LDI register immediate`
            #Machine code:
            ###```
            #10000010 00000rrr iiiiiiii
               # 82 0r ii
            

            #elif PRN`


            

            ## after running the instructions, 
            ## PC is updates to point at next instruction
            self.PC += 1
            #print(self.PC)

            #The number of bytes an instruction uses can be determined from the two high bits (bits 6-7)
            #  of the instruction opcode. See the LS-8 spec for details.

    def ram_read(self, address):
        return self.ram[address]
        #pass

    def ram_write(self, value, address):
        self.ram[address] = value
        #pass


