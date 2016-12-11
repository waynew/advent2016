import time
from collections import namedtuple
from functools import lru_cache

data = '''
The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator, a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.
'''.strip()

data = '''
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
'''.strip()

        
items = {
    'H-C': 1,
    'L-C': 1,
    'H-G': 2,
    'L-G': 3,
}

target = {
    'PL-G': 1,
    'TH-G': 1,
    'TH-C': 1,
    'PR-G': 1,
    'RU-G': 1,
    'RU-C': 1,
    'CO-G': 1,
    'CO-C': 1,
    'PL-C': 2,
    'PR-C': 2,
}

items = {
    'PL-G': 4,
    'TH-G': 4,
    'TH-C': 4,
    'PR-G': 4,
    'RU-G': 4,
    'RU-C': 4,
    'CO-G': 4,
    'CO-C': 4,
    'PL-C': 4,
    'PR-C': 4,
}

def floor_to_text(items, floors=4, cur_floor=1):
    text = []
    for floor in range(1, floors+1):
        if floor == cur_floor:
            elevator = '\x1b[;41m{}\x1b[0m'.format(floor)
        else:
            elevator = floor
        text.insert(0, '{} {}'.format(elevator, ' '.join(colorize(item, items) if items[item] == floor else '  . ' for item in sorted(items))))

    return '\n'.join(text)


def colorize(item, items):
    stuff_on_floor = [i for i in items if items[i] == items[item] and i != item]
    if item.endswith('-C') and stuff_on_floor and not item.replace('-C', '-G') in stuff_on_floor:
        return '\x1b[;31m{}\x1b[0m'.format(item)
    elif item.endswith('-G') and any(chip.replace('-C', '-G') not in stuff_on_floor for chip in stuff_on_floor if chip.endswith('-C')):
        return '\x1b[;31m{}\x1b[0m'.format(item)
    elif can_go_up(item, items):
        return '\x1b[;32m{}\x1b[0m'.format(item)
    else:
        return '\x1b[;33m{}\x1b[0m'.format(item)


def can_go_up(item, items):
    next_floor = items[item]+1
    stuff_on_floor = [i for i in items if items[i] == items[item]]
    stuff_on_next_floor = [i for i in items if items[i] == next_floor]
    if not stuff_on_next_floor:
        return True
    elif ((item.endswith('-C') and item.replace('-C', '-G') in stuff_on_floor)
            or item.endswith('-G') and item.replace('-G', '-C') in stuff_on_floor):
        return True
    elif item.endswith('-C') and item.replace('-C', '-G') in stuff_on_next_floor:
        return True
    return False


def fried(items):
    for floor in range(1, 5):
        stuff_on_floor = [i for i in items if items[i] == floor]
        for chip in (chip for chip in stuff_on_floor if chip.endswith('-C')):
            if chip.replace('-C', '-G') not in stuff_on_floor and any(thing.endswith('-G') for thing in stuff_on_floor):
                return True


move_count = 0
cur_floor = 4

Hand = namedtuple('Hand', 'left,right')

moves = [
    (Hand('H-C', None), 1),
    (Hand('H-C', 'H-G'), 1),
    (Hand('H-C', None), -1),
    (Hand('H-C', None), -1),
    (Hand('H-C', 'L-C'), 1),
    (Hand('H-C', 'L-C'), 1),
    (Hand('H-C', 'L-C'), 1),
    (Hand('H-C', None), -1),
    (Hand('L-G', 'H-G'), 1),
    (Hand('L-C', None), -1),
    (Hand('L-C', 'H-C'), 1),
]

moves = (
    (Hand('CO-C', 'PL-C'), -1),
    (Hand(None  , 'PL-C'), 1),
    (Hand('PL-C', 'PR-C'), -1),
    (Hand(None  , 'PL-C'), 1),
    (Hand('PL-C', 'RU-C'), -1),
    (Hand(None  , 'PL-C'), 1),
    (Hand('PL-C', 'TH-C'), -1),
    (Hand('RU-C', 'TH-C'), -1),
    (Hand(None  , 'RU-C'), 1),
    (Hand('RU-C', 'PR-C'), -1),
    (Hand(None  , 'RU-C'), 1),
    (Hand('RU-C', 'PL-C'), -1),
    (Hand(None  , 'RU-C'), 1),
    (Hand('RU-C', 'CO-C'), -1),
    (Hand(None  , 'CO-C'), 1),
    (Hand(None  , 'CO-C'), 1),
    (Hand('CO-G'  , 'CO-C'), -1),
    (Hand(None  , 'CO-G'), 1),
    (Hand('CO-G'  , 'PL-G'), -1),
    (Hand('CO-G'  , 'CO-C'), 1),
    (Hand('PR-G'  , 'RU-G'), -1),
    (Hand(None    , 'RU-G'), 1),
    (Hand('TH-G'  , 'RU-G'), -1),
    (Hand(None    , 'RU-G'), 1),
    (Hand('CO-G'  , 'CO-C'), -1),
    (Hand(None    , 'CO-C'), -1),
    (Hand(None    , 'PR-C'), 1),
    (Hand('PR-G'  , 'PR-C'), 1),
    (Hand(None    , 'RU-G'), -1),
)


print('Target:')
print(floor_to_text(target))
print('\n'+'*'*50)
print('\n'*3)
print('\x1b[3A', end='')
print(floor_to_text(items, cur_floor=cur_floor), end='')
for move in moves:
    time.sleep(0.1)
    hand, count = move
    cur_floor += count
    if hand.left:
        items[hand.left] += count

    if hand.right:
        items[hand.right] += count
    print('\x1b[3A', end='\r')
    print(floor_to_text(items, cur_floor=cur_floor), end='\r')
    if fried(items):
        print('\nFried!')
        break
    if items == target:
        print('\nWon in {} steps!'.format(len(moves)))
        
