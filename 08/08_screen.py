pixels = [list(None for _ in range(50))
          for _ in range(6)
          ]

#pixels = [list(None for _ in range(7))
#          for _ in range(3)
#          ]


with open('input.txt') as f:
    instructions = f.readlines()


#instructions = [
#    'rect 3x2',
#    'rotate column x=1 by 1',
#    'rotate row y=0 by 4',
#    'rotate row x=1 by 1',
#]

def debug(pixels):
    return '\n'.join(''.join('#' if cell else '.' for cell in row) for row in pixels)

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
            for _ in range(amount):
                #new_vals = [pixels[(row+1)%len(pixels)][col] for row in range(len(pixels))]
                new_vals = [pixels[row-1 if row > 0 else len(pixels)-1][col] for row in range(len(pixels))]
                print(new_vals)
                for row in range(len(pixels)):
                    pixels[row][col] = new_vals[row]
                    print(row, (row+1)%len(pixels), col)

        elif rest.startswith('row'):
            row, amount = (int(val) for val in rest.split('=')[-1].split(' by '))
            for _ in range(amount):
                pixels[row] = pixels[row][-1:] + pixels[row][:-1]
        else:
            assert False, 'Unknown direction '+rest
    else:
        assert False, 'Unknown instruction '+op
    print()
    print(instruction)
    print(debug(pixels))

print('pixels lit:', sum(sum(1 for x in row if x) for row in pixels))
