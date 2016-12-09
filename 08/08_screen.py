from collections import deque

def debug(pixels):
    return '\n'.join(''.join('\x1b[32m#\x1b[0m' if cell else '.' for cell in row) for row in pixels)

def display(instructions, width=50, height=6, sync_rate=0.1):
    pixels = [deque(None for _ in range(width))
              for _ in range(height)
              ]

    lit_count = 0
    print(debug(pixels), end='')
    for instruction in instructions:
        op, _, rest = instruction.partition(' ')
        if op == 'rect':
            width, height = [int(val) for val in rest.split('x')]
            for x in range(width):
                for y in range(height):
                    pixels[y][x] = True
        elif op == 'rotate':
            if rest.startswith('column'):
                col, amount = (int(val) for val in rest.split('=')[-1].split(' by '))
                pixels = list(deque(z) for z in zip(*pixels[::-1]))
                pixels[col].rotate(-amount)
                pixels = list(reversed(list(deque(z) for z in zip(*pixels))))

            elif rest.startswith('row'):
                row, amount = (int(val) for val in rest.split('=')[-1].split(' by '))
                pixels[row].rotate(amount)
            else:
                assert False, 'Unknown direction '+rest
        else:
            assert False, 'Unknown instruction '+op
        lit_count = sum(sum(1 for x in row if x) for row in pixels)
        print('\x1b[5A', end='\r')
        print(debug(pixels), end='\r')
        print('\n{:*<50}'.format('*** {:>3} '.format(lit_count)), end='\x1b[1A')
        import time; time.sleep(sync_rate)

    return lit_count


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = f.readlines()
        for _ in range(8):
            print('*'*50)
        print('\x1b[7A', end='\r')
        pixels_lit = display(instructions, sync_rate=0.1)
        print()
