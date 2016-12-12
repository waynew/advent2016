import time
import sys
import logging


def debug(cmd, op1, op2, registers):
    for register in 'abcd':
        if register in (op1, op2):
            fmt = '\x1b[32m{}: {:>6}\x1b[0m'
        else:
            fmt = '{}: {:>6}'
        print(fmt.format(register, registers[register]), end=' ')


with open('input.txt') as f:
    instructions = f.readlines()


def show_progress(instructions, program_counter):
    for i, instruction in enumerate(instructions):
        print('\x1b[32m{:<3}\x1b[0m {}'.format('-->' if i == program_counter else '', instruction.strip()))


CLOCK_SLOWDOWN = 0.0
debug = False
registers = dict.fromkeys('abcd', 0)
registers['c'] = 1
program_counter = 0

if debug:
    print('\n'*(len(instructions)+1), end='')

while program_counter < len(instructions):
    instruction = instructions[program_counter].split()
    instruction.extend([None, None])
    cmd, op1, op2, *_ = instruction

    if debug:
        print('\x1b[{}A'.format(len(instructions)+1), end='')
        show_progress(instructions, program_counter)
        print(debug(cmd, op1, op2, registers))
        sys.stdout.flush()
        time.sleep(CLOCK_SLOWDOWN)

    if cmd == 'cpy':
        if op1.isdigit():
            registers[op2] = int(op1)
        else:
            registers[op2] = registers[op1]
    elif cmd == 'inc':
        registers[op1] += 1
    elif cmd == 'dec':
        registers[op1] -= 1
    elif cmd == 'jnz':
        offset = int(op2) - 1
        #if offset < 0:
        #    offset -= 1
        if op1.isdigit():
            if op1 != '0':
                program_counter += offset
        elif registers[op1] != 0:
            program_counter += offset

    program_counter += 1

print(registers)
