import sys

# Write a program in Python that runs programs

# Instructions and their numeric representation
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRM in the LS8
ADD = 5	# Add two registers, r0 += r1

memory = [0] * 256	# RAM storage

register = [0] * 8  # like variables R0-R7

running = True  # Boolean to stop the program from running

pc = 0  # Program Counter, the address of the current instruction in memory

# Load program into memory
address = 0

with open(sys.argv[1]) as f:
	for line in f:
		string_val = line.split("#")[0].strip()
		if string_val == '':
			continue
		value = int(string_val, 10)
		print(value)
		memory[address] = value

		address += 1


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

    elif inst == ADD:
        reg_num_a = memory[pc + 1]
        reg_num_b = memory[pc + 2]

        register[reg_num_a] += register[reg_num_b]

        pc += 3

    elif inst == HALT:
        running = False

    else:
        print(f"Unknown instruction {inst} at address {pc}")
        exit(1)