pinpad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

loc = [1,1]

hidden_code = '''
ULL
RRDDD
LURDL
UUUUD
'''
hidden_code = hidden_code.strip().split('\n')

code = []
for line in hidden_code:
    for dir in line:
        if dir == 'U':
            loc[0] = max(0, loc[0]-1)
        elif dir == 'D':
            loc[0] = min(2, loc[0]+1)
        elif dir == 'L':
            loc[1] = max(0, loc[1]-1)
        elif dir == 'R':
            loc[1] = min(2, loc[1]+1)
        else:
            assert False, 'Code {!r} was unexpected'.format(dir)
    code.append(pinpad[loc[0]][loc[1]])

print(''.join(code))
