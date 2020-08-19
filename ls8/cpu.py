"""CPU functionality."""

'''
### Day 2: Add the ability to load files dynamically, get `mult.ls8` running

- [ ] Un-hardcode the machine code
- [ ] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [ ] Implement a Multiply instruction (run `mult.ls8`)
'''

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
        self.general_purpose_register = [0] * 8
        #pass

    def load(self):
        """Load a program into memory."""

        address = 0

        #print(sys.argv)

        #Bonus: check to make sure the user has put a command line argument where you expect, and print an error and exit if they didn't.
        program = sys.argv[1]

        with open(program) as f:
            for line in f:
                comment_split = line.split("#")
                n = comment_split[0].strip()
                x = int(n, 2)
                self.ram[address] = x
                address += 1
                # print(x)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        #     print(instruction)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.general_purpose_register[reg_a] *= self.general_purpose_register[reg_b]
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

        #print(f'RAM: {self.ram}')
        #print(f'General Purpose Register: {self.general_purpose_register}')


        # dpending on the value of the opcode
        # perform the actions needed for the instruction
        while self.PC < 256:
            #print(f'PC: {self.PC}')
            # print(f'RAM: {self.ram}')
            # print(f'General Purpose Register: {self.general_purpose_register}')


            operand_a = self.ram_read(self.PC+1)
            operand_b = self.ram_read(self.PC+2)

            #instruction register
            IR = self.ram[self.PC]

            #if HLT:
            if IR == 0b00000001:
                print("HLT!!!")
                exit()

            #elif LDI
            elif IR == 0b10000010:
                #Set the value of a register to an integer.
                print("LDI")
                #IR = int(IR)
                self.general_purpose_register[operand_a] = operand_b
                self.PC += 2
                #print(self.general_purpose_register)


            #elif PRN`
            elif IR == 0b01000111:
                print("PRN")
                print(self.general_purpose_register[operand_a])
                self.PC += 1
            
            elif IR == 0b10100010:
                print("MUL")
                self.alu(op="MUL", reg_a=operand_a, reg_b=operand_b)
                self.PC += 2
            

            ## after running the instructions, 
            ## PC is updates to point at next instruction
            self.PC += 1
            #print(self.PC)

            #The number of bytes an instruction uses can be determined from the two high bits (bits 6-7)
            #  of the instruction opcode. See the LS-8 spec for details.

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value


