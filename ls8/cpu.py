"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.stack_pointer = 255
        self.ops = {}
        self.ops[LDI] = self.LDI
        self.ops[PRN] = self.PRN
        self.ops[HLT] = self.HLT
        self.ops[MUL] = self.MUL
        self.running = False
        self.ops[POP] = self.POP
        self.ops[PUSH] = self.PUSH
        self.ops[CALL] = self.CALL
        self.ops[RET] = self.RET
        self.ops[ADD] = self.ADD
        
        
        
    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.ram_write(address, value)
        self.pc += 3
        
    def PRN(self):
        address = self.ram[self.pc + 1]
        self.ram_read(address)
        self.pc += 2
        
    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3
        
    def HLT(self):
        self.running = False
        
    def PUSH(self):
        self.reg[7] -= 1
        
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        
        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value
        
        self.pc += 2
        
    def POP(self):
        address_to_pop = self.reg[7]
        value = self.ram[address_to_pop]
        
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        
        self.reg[7] += 1
        
        self.pc += 2
        
    def CALL(self):
        ret_addr = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = ret_addr
        
        reg_num = self.ram[self.pc + 1]
        self.pc = self.reg[reg_num]
        
    def RET(self):
        ret_addr = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        self.pc = ret_addr

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('ADD', reg_a, reg_b)
        self.pc += 3
        
    def load(self):
        """Load a program into memory."""

        address = 0
        
            
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)
            
        try:
            with open('examples/' + sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()
                    
                    if len(temp) == 0:
                        continue
                    
                    if temp[0][0] == '#':
                        continue
                    
                    try:
                        self.ram[address] = int(temp[0], 2)
                        
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)
                        
                        
                    address += 1
                
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(1)
            
        if address == 0:
            print("Program was empty!")
            sys.exit(3)
              
            
    def ram_read(self, address):
        print(self.reg[address])
    
    def ram_write(self, address, value):
        self.reg[address] = value
        
    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

        # print()

    def run(self):
        """Run the CPU."""
        
        
        self.running = True
        
        while self.running:
            
            ir = self.ram[self.pc]
            
            self.ops[ir]()
        
        # while running:
            # ir = self.ram_read(self.pc)
            # operand_a = self.ram_read(self.pc + 1)
            # operand_b = self.ram_read(self.pc + 1)
            
            # if ir == 0b10000010:
            #     reg_num = self.ram[self.pc + 1]
            #     value = self.ram[self.pc + 2]
                
            #     self.reg[reg_num] = value
                
            #     self.pc += 3
                
            # elif ir == 0b01000111:
            #     reg_num = self.ram[self.pc + 1]
            #     print(self.reg[reg_num])
                
            #     self.pc += 2
                
            # elif ir == 0b10100010:
            #     reg_a = self.ram[self.pc + 1]
            #     reg_b = self.ram[self.pc + 2]
            #     self.alu('MUL', reg_a, reg_b)
                
            #     self.pc += 3
                
            # elif ir == 0b00000001:
            #     running = False
