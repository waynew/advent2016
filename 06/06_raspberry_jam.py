from collections import Counter

counters = []
with open('input.txt') as f:
    counters = [Counter() for _ in next(f)]
    f.seek(0)
    for line in f:
        for i, char in enumerate(line):
            counters[i][char] += 1

print(''.join(c.most_common()[-1][0] for c in counters))
