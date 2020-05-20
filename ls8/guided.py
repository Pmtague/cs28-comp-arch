# Write a program in Python that runs programs

# Instructions and their numeric representation
import sys
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRM in the LS8

# Store Instructions in memory, what is in memory determines how the program below runs
memory = [
    PRINT_BEEJ,
    SAVE_REG,  # Save R0, 37		store 37 in R0		opcode
    0, 	# R0		operand ("argument")
    37,  # 37		operand
    PRINT_BEEJ,
    PRINT_REG,  # PRINT_REG R0
    0,
    HALT
]

register = [0] * 8  # like variables R0-R7

pc = 0  # Program Counter, the address of the current instruction
running = True  # Boolean to stop the program from running

while running:

    inst = memory[pc]

    if inst == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif inst == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2

    elif inst == HALT:
        running = False

    else:
        print("Unknown instruction")
        running = False

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))
