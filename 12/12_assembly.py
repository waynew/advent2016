from collections import Counter
import time
import sys
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('tmp.log'))
#logger.setLevel(logging.DEBUG)


def debug(cmd, op1, op2, registers):
    for register in 'abcd':
        if register in (op1, op2):
            logger.debug('register %r op1 %r op2 %r', register, op1, op2)
            fmt = '\x1b[32m{}: {:>6}\x1b[0m'
        else:
            fmt = '{}: {:>6}'
        print(fmt.format(register, registers[register]), end=' ')


with open('input.txt') as f:
    instructions = f.readlines()


def show_progress(instructions, program_counter):
    for i, instruction in enumerate(instructions):
        print('\x1b[32m{:<3}\x1b[0m {}'.format('-->' if i == program_counter else '', instruction.strip()))


CLOCK_SLOWDOWN = 0.5
registers = Counter()
print('\n'*(len(instructions)+1), end='')
program_counter = 0
while program_counter < len(instructions):
    logger.debug('PC: %r registers: %r', program_counter, registers)
    instruction = instructions[program_counter].split()
    instruction.extend([None, None])
    cmd, op1, op2, *_ = instruction

    print('\x1b[{}A'.format(len(instructions)+1), end='')
    show_progress(instructions, program_counter)
    print(debug(cmd, op1, op2, registers))
    sys.stdout.flush()

    if cmd == 'cpy':
        logger.debug('copying %r to %r', op1, op2)
        if op1.isdigit():
            registers[op2] = int(op1)
        else:
            registers[op2] = registers[op1]
    elif cmd == 'inc':
        logger.debug('incrementing %r from %r to %r', op1, registers[op1], registers[op1]+1)
        registers[op1] += 1
    elif cmd == 'dec':
        logger.debug('decrementing %r from %r to %r', op1, registers[op1], registers[op1]-1)
        registers[op1] -= 1
    elif cmd == 'jnz':
        offset = int(op2)
        #if offset < 0:
        #    offset -= 1
        if op1.isdigit():
            if op1 != '0':
                program_counter += offset
        if registers[op1] != 0:
            program_counter += offset
            logger.info('%r is %r so setting program counter to %r',
                        op1, registers[op1], program_counter)
        else:
            logger.info('%r is %r zero so program counter continues %r',
                        op1, registers[op1], program_counter)

    program_counter += 1
    time.sleep(CLOCK_SLOWDOWN)
