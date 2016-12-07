import re

def get_abas(text):
    abas = []
    for start in range(len(text)-2):
        segment = text[start:start+3]
        if segment.count(segment[0]) == 2 and segment == segment[::-1]:
            abas.append(segment)
    return abas


def aba_to_bab(aba):
    return aba[1]+aba[:-1]


def supports_ssl(address):
    hypernets = re.findall(r'\[(.*?)]', address)
    for hypernet in hypernets:
        address = address.replace('[{}]'.format(hypernet), ' ')
    other_bits = address.split()
    abas = []
    for bit in other_bits:
        abas.extend(get_abas(bit))
    babs = [aba_to_bab(aba) for aba in abas]
    for bab in babs:
        for hypernet in hypernets:
            if bab in hypernet:
                return True
    return False

count = 0
with open('input.txt') as f:
    for line in f:
        if supports_ssl(line):
            count += 1
print('Supports SSL:', count)
