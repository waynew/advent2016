import hashlib
from collections import defaultdict
from functools import lru_cache


@lru_cache()
def hashify(index, salt='abc{}'):
    md5 = hashlib.md5(salt.format(index).encode())
    return md5.hexdigest()
    

def triplets(curse):
    triples = set()
    for i in range(len(curse)-3):
        substr = curse[i:i+3]
        if substr.count(substr[0]) == len(substr):
            triples.add(substr)
    return triples


def has_quint(char, curse):
    for i in range(len(curse)-5):
        substr = curse[i:i+5]
        if substr.count(char) == len(substr):
            return True


def get_key(curse):
    triples = triplets(curse)
    for triplet in triples:
        for n in range(index, index+1000):
            if has_quint(triplet[0], hashify(n, salt=salt)):
                return (index, n, curse, hashify(n))
    return None


salt = 'abc{}'
keys = []
index = 0
while len(keys) < 65:
    potato = hashify(index, salt=salt)
    key = get_key(potato)
    if key is not None:
        keys.append(key)
        print(keys[-1])
    index += 1
print(keys)
