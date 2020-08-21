"""CPU functionality."""

'''
Minimum Viable Product
Your finished project must include all of the following requirements:

[X] Add the CMP instruction and equal flag to your LS-8.

[X] Add the JMP instruction.

[X] Add the JEQ instructions.

[ ] Add JNE 
'''
### WILL'S SUPER DOPE LS-8 COMPUTER
import sys

#Opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
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
        self.flag_register = [0] * 8
       
        #Branch Table initialization
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

    def handle_HLT(self, IR, operand_a, operand_b):
        print("handle HLT")
        if IR == HLT:
            self.halted = True

    #Set the value of a register to an integer.
    def handle_LDI(self, IR, operand_a, operand_b):
        print("handle LDI")
        self.general_purpose_register[operand_a] = operand_b

    def handle_PRN(self, IR, operand_a, operand_b=None):
        print("handle PRN")
        print(self.general_purpose_register[operand_a])

    def handle_ADD(self, IR, operand_a, operand_b):
        print("handle ADD")
        self.alu(op="ADD", reg_a=operand_a, reg_b=operand_b)

    def handle_MUL(self, IR, operand_a, operand_b):
        print("handle MUL")
        self.alu(op="MUL", reg_a=operand_a, reg_b=operand_b)

    def handle_PUSH(self, IR, operand_a, operand_b=None):
        print("handle PUSH")
        value = self.general_purpose_register[operand_a]
        #decrement stack pointer
        self.general_purpose_register[self.stack_pointer] -= 1
        #insert value onto stack
        self.ram[self.general_purpose_register[self.stack_pointer]] = value

    def handle_POP(self, IR, operand_a, operand_b=None):
        print("handle POP")
        #value is grabbed from where the stack pointer is pointing in the RAM
        value = self.ram[self.general_purpose_register[self.stack_pointer]]
        #increment stack pointer
        self.general_purpose_register[self.stack_pointer] += 1
        #put the value back on the register
        self.general_purpose_register[operand_a] = value

    def handle_CALL(self, IR, operand_a, operand_b=None):
        print("handle CALL")

        #decrement stack pointer
        self.general_purpose_register[self.stack_pointer] -= 1
        # The address of the instruction directly after CALL is pushed onto the stack.
        # This allows us to return to where we left off when the subroutine finishes executing.
        self.ram[self.general_purpose_register[self.stack_pointer]] = self.PC+2
        # The PC is set to the address stored in the given register.
        # We jump to that location in RAM and execute the first instruction in the subroutine. 
        # The PC can move forward or backwards from its current location.
        self.PC = self.general_purpose_register[operand_a]

    def handle_RET(self, IR, operand_a, operand_b):
        print("handle RET")
        # the PC is set to the value saved in the stack
        self.PC = self.ram[self.general_purpose_register[self.stack_pointer]]
        #increment stack pointer
        self.general_purpose_register[self.stack_pointer] += 1
        # print(self.PC)

    def handle_CMP(self, IR, operand_a, operand_b):
        '''
        Compare the values in two registers.
        If they are equal, set the Equal E flag to 1, otherwise set it to 0.
        If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
        If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
        
        FL bits: 00000LGE
        L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.        
        '''
        print("handle CMP")
        reg_A = self.general_purpose_register[operand_a]
        reg_B = self.general_purpose_register[operand_b]

        #this resets the flag register to all 0s
        self.flag_register = [0] * 8
        # logic handling
        if reg_A == reg_B:
            self.flag_register[-1] = 1
        if reg_A < reg_B:
            self.flag_register[-3] = 1
        if reg_A > reg_B:
            self.flag_register[-2] = 1

        # print(f'FLAG REGISTER: {self.flag_register}')

    def handle_JMP(self, IR, operand_a, operand_b):
        '''
        Jump to the address stored in the given register.
        Set the PC to the address stored in the given register.
        '''
        print("handle JMP")
        # print(self.general_purpose_register)
        self.PC = self.general_purpose_register[operand_a]
        # print(self.PC)

    def handle_JEQ(self, IR, operand_a, operand_b):
        '''
        If equal flag is set (true), jump to the address stored in the given register.
        '''
        print("handle JEQ")

        # print(self.flag_register)

        if self.flag_register[-1] == 1:
            # print("JUMPING!")
            self.PC = self.general_purpose_register[operand_a]
        else:
            IR = self.ram[self.PC]
            instruction_length = ((IR >> 6) & 0b11) + 1
            self.PC += instruction_length

    def handle_JNE(self, IR, operand_a, operand_b):
        '''
        If `E` flag is clear (false, 0), jump to the address stored in the given register.
        '''
        print("handle JNE")
        # print(self.general_purpose_register)
        if self.flag_register[-1] == 0:
            self.PC = self.general_purpose_register[operand_a]
            # print(self.PC)
        else:
            IR = self.ram[self.PC]
            instruction_length = ((IR >> 6) & 0b11) + 1
            self.PC += instruction_length
        # print(self.PC)

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
            unusual_commands = [CALL, RET, JMP, JEQ, JNE]
            if IR not in unusual_commands:
                self.PC += instruction_length
            # print(f'GENERAL REGISTER: {self.general_purpose_register}')