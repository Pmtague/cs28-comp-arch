"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.sp = 7
        # self.int_status = self.register[6]
        # self.int_mask = self.register[5]
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

    # Push value from register address into ram address of stack pointer
    def push(self, register):

        # Decrement Stack Pointer (SP)
        self.sp -= 1

        # Store current value of SP
        ram_address = self.register[self.sp]

        # Add stored SP value in RAM (Add to stack at designated area of RAM?)
        self.ram[ram_address] = self.register[register]

    # Retreive value from RAM address pointed to by the SP
    def pop(self, register):
        pass
        # 


    # Grabs program from example directory and loads it into memory
    def load(self, file):
        """Load a program into memory."""

        try:

            # Address counter for looping
            address = 0

            # Open file with auto-close
            with open(file) as f:

                # Loop through each line in the file
                for line in f:

                    # Get rid of anything in the line that starts with #
                    split_line = line.split("#")

                    # Get rid of any leading or trailing spaces
                    formatted_line = split_line[0].strip()

                    # If the current line is 8 characters long
                    if len(formatted_line) == 8:

                        # Convert the line to a binary integer
                        value = int(formatted_line, 2)

                        # Add that value to the current ram address
                        self.ram[address] = value

                    # If the current line is not 8 characters long
                    else:
                        continue

                    # Move to the next memory address
                    address += 1

        except FileNotFoundError:

            print(f"{file} not found")
            sys.exit(2)

    # ALU = arithmetic logic unit: performs basic math and logic operations
    def alu(self, op, register_a, register_b):
        """ALU operations."""

        if op == "ADD":
            self.register[register_a] += self.register[register_b]

        elif op == "SUB":
            self.register[register_a] -= self.register[register_b]

        elif op == "MUL":
            self.register[register_a] *= self.register[register_b]

        elif op == "AND":
            self.register[register_a] = self.register[register_a] and self.register[register_b]

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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # Boolean to control the running process
        running = True

        # Instructions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        SUB = 0b10100001
        AND = 0b10101000
        PUSH = 0b01000101
        POP = 0b01000110

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

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)
                self.pc += 3

            elif ir == PRN:
                value = self.register[operand_a]
                print(value)
                self.pc += 2
            
            elif ir == AND:
                self.alu("AND", operand_a, operand_b)
                self.pc += 3
            
            elif ir == PUSH:
                self.push()
                self.pc += 2

            elif ir == POP:
                self.pop()
                self.pc += 2

            elif ir == HLT:
                running = False

            else:
                print("Unknown instruction")
                running = False
