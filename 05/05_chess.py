import hashlib

puzzle_in = 'abc'
password = ['_']*8
fmt = '{}{}{}{}{}{}{}{}'

def red(letter):
    return '\x1b[31m'+letter


def green(letter):
    return '\x1b[32m'+letter


index = 0
while password.count('_'):
    md5 = hashlib.md5()
    md5.update((puzzle_in+str(index)).encode())
    digest = md5.hexdigest()
    if digest.startswith('00000'):
        try:
            pw_index = int(digest[5])
            char = digest[6]
            if password[pw_index] == '_':
                password[pw_index] = char
        except (IndexError, ValueError) as e:
            pass
        else:
            fake = [red(f) if r == '_' else green(r) for f, r in zip(digest, password)]
            print('Hacking...', fmt.format(*fake), end='\x1b[0m\r\a')

    if not index % 10000:
        fake = [red(f) if r == '_' else green(r) for f, r in zip(digest, password)]
        print('Hacking...', fmt.format(*fake), end='\x1b[0m\r')
    index += 1

print('Hacked!   ', green(fmt.format(*password)), end='\x1b[0m\n\a')
