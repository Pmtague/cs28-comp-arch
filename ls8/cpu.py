"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.sp = 7
        self.register[self.sp] = 0xF4
        self.pc = 0 # Index of current instruction
        # self.fl = 0b00000000

        # self.instructions = {
        #     ADD : 0b10100000,
        #     AND : 0b10101000,
        #     CALL : 0b01010000,
        #     CMP : 0b10100111,
        #     DEC : 0b01100110,
        #     DIV : 0b10100011,
        #     HLT : 0b00000001,
        #     INC : 0b01100101,
        #     INT : 0b01010010,
        #     IRET : 0b00010011,
        #     JEQ : 0b01010101,
        #     JGE : 0b01011010,
        #     JGT : 0b01010111,
        #     JLE : 0b01011001,
        #     JLT : 0b01011000,
        #     JMP : 0b01010100,
        #     JNE : 0b01010110,
        #     LD : 0b10000011,
        #     LDI : 0b10000010,
        #     MOD : 0b10100100,
        #     MUL : 0b10100010,
        #     NOP : 0b00000000,
        #     NOT : 0b01101001,
        #     OR : 0b10101010,
        #     POP : 0b01000110,
        #     PRA : 0b01001000,
        #     PRN : 0b01000111,
        #     PUSH : 0b01000101,
        #     RET : 0b00010001,
        #     SHL : 0b10101100,
        #     SHR : 0b10101101,
        #     ST : 0b10000100,
        #     SUB : 0b10100001,
        #     XOR : 0b10101011
        # }

    # Returns the value at the given memory address
    def ram_read(self, address):
        return self.ram[address]

    # Writes the given value to the given memory address
    def ram_write(self, value, address):
        self.ram[address] = value

    # Push value from register address into ram address of stack pointer
    def push(self, register):

        # Decrement Stack Pointer (SP)
        self.register[self.sp] -= 1

        # Get the value from the given register
        value = self.register[register]

        # Store the top of stack address which is always in the SP slot of the registry
        top_of_stack_addr = self.register[self.sp]

        # Add stored register value to RAM (Add to stack at designated area of RAM?)
        self.ram[top_of_stack_addr] = value

    # Retreive value from RAM address pointed to by the SP and input into given register
    def pop(self, register):

        # Get the value from the stack pointer
        top_of_stack_addr = self.ram[self.register[self.sp]]

        # Add the value to the register
        self.register[register] = top_of_stack_addr

        # Increment SP
        self.register[self.sp] += 1

    # Grabs program from example directory and loads it into memory
    def load(self, file):

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
                        print("RAM Instructions from Program Load",
                        self.ram[address])

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

        # elif op == "DIV":
        #     if self.register[register_b] == 0:
        #         print(f'Dividing by 0 is not allowed')
        #         exit(1)
            # else:
            #     self.register[register_a] /= self.register[register_b]

        # elif op == "MOD":
        #     if self.register[register_b] == 0:
        #         print(f'Dividing by 0 is not allowed')
        #         exit(1)
        #     else:
        #         self. register[register_a] = self.register[register_a] % self.register[register_b]

        # elif op == "AND":
        #     self.register[register_a] = self.register[register_a] & self.register[register_b]

        # elif op == "OR":
        #     self.register[register_a] = self.register[register_a] | self.register[register_b]

        # elif op == "NOT":
        #     self.register[register_a] = self.register[register_a] ~ self.register[register_b]

        # elif op == "XOR":
        #     self.register[register_a] = self.register[register_a] ^ self.register[register_b]

        # elif op == "CMP":
        #     if self.register[register_a] == self.register[register_b]:
        #             self.fl = self.fl | 0b00000001
                
        #     elif self.register[register_a] < self.register[register_b]:
        #         self.fl = self.fl | 0b00000100

        #     elif self.register[register_a] > self.register[register_b]:
        #         self.fl = self.fl | 0b00000010
        #     else:
        #         self.fl = 0b00000000

        # elif op == "DEC":
        #     self.register[register_a] -= 1

        # elif op == "INC":
        #     self.register[register_a] += 1

        # elif op == "SHL":
        #     self.register[register_a] << self.register[register_b]

        # elif op == "SHR":
        #     self.register[register_a] >> self.register[register_b]

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
        ADD = 0b10100000
        AND = 0b10101000
        CALL = 0b01010000
        CMP = 0b10100111
        DEC = 0b01100110
        DIV = 0b10100011
        HLT = 0b00000001
        INC = 0b01100101
        INT = 0b01010010
        IRET = 0b00010011
        JEQ = 0b01010101
        JGE = 0b01011010
        JGT = 0b01010111
        JLE = 0b01011001
        JLT = 0b01011000
        JMP = 0b01010100
        JNE = 0b01010110
        LD = 0b10000011
        LDI = 0b10000010
        MOD = 0b10100100
        MUL = 0b10100010
        NOP = 0b00000000
        NOT = 0b01101001
        OR = 0b10101010
        POP = 0b01000110
        PRA = 0b01001000
        PRN = 0b01000111
        PUSH = 0b01000101
        RET = 0b00010001
        SHL = 0b10101100
        SHR = 0b10101101
        ST = 0b10000100
        SUB = 0b10100001
        XOR = 0b10101011

        # Some instructions require up to the next two bytes of data after the PC in memory to perform operations on.
        # Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI).

        while running:

            # Set instruction to a variable
            ir = self.ram_read(self.pc)
            print("PC", self.ram_read(self.pc))

            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b for use in instructions
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Set the value of a register to an integer
            if ir == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3

            # Multiply two given values
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # Add two given values
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            # Subtract two given values
            # elif ir == SUB:
            #     self.alu("SUB", operand_a, operand_b)
            #     self.pc += 3

            # Print the value at the given location
            elif ir == PRN:
                value = self.register[operand_a]
                print(value)
                self.pc += 2

            elif ir == PUSH:
                self.push(operand_a)
                self.pc += 2

            elif ir == POP:
                self.pop(operand_a)
                self.pc += 2

            elif ir == CALL:
                return_addr = self.pc + 2

                self.register[self.sp] -= 1
                top_of_stack_addr = self.register[self.sp]
                self.ram[top_of_stack_addr] = return_addr

                reg_num = self.ram[operand_a]
                subroutine_addr = self.register[reg_num]

                self.pc = subroutine_addr

            elif ir == RET:
                return_addr = self.ram[self.register[self.sp]]
                print("Return Address", return_addr)
                print("Expecting", self.ram[self.register[self.sp]])
                self.register[self.sp] += 1
                self.pc = return_addr
                print("PC at end of RET", self.pc)

            # elif ir == CMP:
            #     self.alu("CMP", operand_a, operand_b)
            #     print("CMP", operand_a)
            #     self.pc += 3

            # elif ir == JMP:
            #     self.pc = self.register[operand_a]
            #     print("PC in JMP", self.pc)

            # elif ir == JEQ:
            #     if self.fl == 0b00000001:
            #         self.pc = self.register[operand_a]
            #         print("PC in JEQ", self.pc)
            
            # elif ir == JNE:
            #     if self.fl == 0b00000000:
            #         self.pc = self.register[operand_a]
            #         print("PC in JNE", self.pc)

            elif ir == HLT:
                running = False

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                exit(1)

# cpu = CPU()
# cpu.run()
