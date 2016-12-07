def is_abba(four):
    return four.count(four[0]) == 2 and four[:2] == ''.join(reversed(four[2:]))


def has_abba(address):
    within_brackets = False
    has_abba = False
    for start in range(len(address)-4):
        if address[start] in '[]':
            within_brackets = not within_brackets
            continue

        if is_abba(address[start:start+4]):
            if within_brackets:
                return True, True
            else:
                has_abba = True
    return has_abba, within_brackets

count = 0
with open('input.txt') as f:
    for line in f:
        supports_tls = has_abba(line.rstrip()) == (True, False)
        if supports_tls:
            count += 1
            print(line, end='')

print('Supports TLS:', count)
