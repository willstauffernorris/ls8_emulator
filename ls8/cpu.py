"""CPU functionality."""
### WILL'S SUPER DOPE LS-8 COMPUTER
import sys

#Opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256
        self.general_purpose_register = [0] * 8
        # Program counter: PC stores the address of the currently executing instruction
        self.PC = 0
        self.halted = False
        self.stack_pointer = 7
        #Branch Table initialization
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP

    def handle_HLT(self, IR, operand_a, operand_b):
        if IR == HLT:
            self.halted = True

    #Set the value of a register to an integer.
    def handle_LDI(self, IR, operand_a, operand_b):
        self.general_purpose_register[operand_a] = operand_b
        # print("LDI")
        #print(self.general_purpose_register)

    def handle_PRN(self, IR, operand_a, operand_b=None):
        print(self.general_purpose_register[operand_a])

    def handle_MUL(self, IR, operand_a, operand_b):
        self.alu(op="MUL", reg_a=operand_a, reg_b=operand_b)

    def handle_PUSH(self, IR, operand_a, operand_b=None):
        # print("PUSH")
        # register_index = self.ram[operand_a]
        # print(f'REGISTER INDEX {register_index}')
        value = self.general_purpose_register[operand_a]
        #print(f'VALUE: {value}')
        # print(f'Operand A {operand_a}')

        # print(f'IR {IR}')
    
        #decrement stack pointer
        self.general_purpose_register[self.stack_pointer] -= 1
        #insert value onto stack
        self.ram[self.general_purpose_register[self.stack_pointer]] = value

        # print(self.ram)
        # print(self.general_purpose_register)

    def handle_POP(self, IR, operand_a, operand_b=None):
        # print("POP")
        #value is grabbed from where the stack pointer is pointing in the RAM
        value = self.ram[self.general_purpose_register[self.stack_pointer]]

        #increment stack pointer
        self.general_purpose_register[self.stack_pointer] += 1

        self.general_purpose_register[operand_a] = value

        # print(self.ram)
        # print(self.general_purpose_register)




    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0
        #Bonus: check to make sure the user has put a command line argument where you expect,
        #  and print an error and exit if they didn't.
        program = sys.argv[1]

        with open(program) as f:
            for line in f:
                comment_split = line.split("#")
                n = comment_split[0].strip()
                #ignore the blank lines
                if n == '':
                    continue
                x = int(n, 2)
                self.ram[address] = x
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.general_purpose_register[reg_a] += self.general_purpose_register[reg_b]

        elif op == "SUB":
            self.general_purpose_register[reg_a] -= self.general_purpose_register[reg_b]

        elif op == "MUL":
            self.general_purpose_register[reg_a] *= self.general_purpose_register[reg_b]
       
        elif op == "DIV":
            self.general_purpose_register[reg_a] //= self.general_purpose_register[reg_b]
        
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

        # print(f'RAM: {self.ram}')
 

        while not self.halted:
            #instruction register
            IR = self.ram[self.PC]
            operand_a = self.ram_read(self.PC+1)
            operand_b = self.ram_read(self.PC+2)
            #I need to understand this part better- what is the '&' sign doing?
            instruction_length = ((IR >> 6) & 0b11) + 1

            if IR in self.branchtable:
                self.branchtable[IR](IR, operand_a, operand_b)

            ## after running the instructions, PC is updates to point at next instruction
            self.PC += instruction_length
            #print(f'REGISTER: {self.general_purpose_register}')
