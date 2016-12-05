import hashlib

puzzle_in = 'abc'
password = ['_']*8
fmt = '{}{}{}{}{}{}{}{}'

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
            print(fmt.format(*password), end='\r\a')

    if not index % 10000:
        print(fmt.format(*password), index, end='\r')
    #print(digest, end='\r')
    index += 1
