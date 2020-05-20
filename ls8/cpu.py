"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.fl = 0
        # self.ir = None
        # self.mar = None
        # self.mdr = None
    
    # Returns the value at the given memory address
    def ram_read(self, address):
        return self.ram[address]

    # Writes the given value to the given memory address
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # Need to be able to run from any program file eventually

        program = [     # Instructions
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # Loops through the program and adds each instruction to a memory address
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # ALU = arithmetic logic unit: performs basic math and logic operations
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

        # Boolean to control the running process
        running = True

        # Instructions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while running:

            # Set instruction to a variable
            instruction = self.ram_read(self.pc)

            # Set the value of a register to an integer
            if instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.register[reg_num] = value
                self.pc += 3

            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                value = self.register[reg_num]
                print(value)
                self.pc += 2

            elif instruction == HLT:
                running = False

            else:
                print("Unknown instruction")
                running = False

