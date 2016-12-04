import re
import string
from collections import Counter


with open('input.txt') as f:
    rooms = [room.strip() for room in f]

#rooms = [
#    'aaaaa-bbb-z-y-x-123[abxyz]',
#    'a-b-c-d-e-f-g-h-987[abcde]',
#    'not-a-real-room-404[oarel]',
#    'totally-real-room-200[decoy]',
#    'qzmt-zixmtkozy-ivhz-343[zimth]',
#]


def parse_room(room):
    checksum = room[-6:-1]
    letters, _, sector_id= room[:-7].rpartition('-')
    sector_id = int(sector_id)
    return letters, sector_id, checksum

def is_decoy_room(room_id, checksum):
    counter = Counter()
    for letter in room_id:
        counter[letter] += 1

    most_common = sorted(counter.most_common(), key=lambda x: (10-x[1], x[0]))

    for checkdigit, count in zip(checksum, most_common):
        if checkdigit != count[0]:
            return True
    return False

def shift_letter(letter, amount):
    if letter == '-':
        return '-'
    offset = (ord(letter)-ord('a')+amount)%26
    return chr(ord('a')+offset)

real_room_sector_sum = 0
for room in rooms:
    room_id, sector_id, checksum = parse_room(room)
    if not is_decoy_room(room_id.replace('-', ''), checksum):
        real_room_sector_sum += sector_id
        real_name = ''.join(shift_letter(l, sector_id) for l in room_id)
        if 'north' in real_name:
            print(real_name, sector_id)

print('Real sector sum: ', real_room_sector_sum)
