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
        # self.mar = None
        # self.mdr = None

    # Returns the value at the given memory address
    def ram_read(self, address):
        return self.ram[address]

    # Writes the given value to the given memory address
    def ram_write(self, value, address):
        self.ram[address] = value

    # Grabs program from example directory and loads it into memory
    def load(self):
        """Load a program into memory."""

        # Address counter for looping
        address = 0

        # path_to_file = "examples/file_name"

        # For now, we've just hardcoded a program:
        # Need to be able to run from any program file eventually

        program = [     # Instructions
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
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
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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

        # Some instructions require up to the next two bytes of data after the PC in memory to perform operations on.
        # Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI).

        while running:

            # Set instruction to a variable
            ir = self.ram_read(self.pc)

            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case
            # the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Set the value of a register to an integer
            if ir == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                value = self.register[operand_a]
                print(value)
                self.pc += 2

            elif ir == HLT:
                running = False

            else:
                print("Unknown instruction")
                running = False
