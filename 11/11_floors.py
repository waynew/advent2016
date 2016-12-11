import time
from collections import namedtuple

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

class Elevator:
    def __init__(self, capacity, floor):
        self.floor = floor
        self.capacity = capacity
        self.items = []

    def go_up(self):
        if self.floor < 4:
            self.floor += 1
        for item in self.items:
            item.floor = self.floor
        
    def go_down(self):
        if self.floor > 1:
            self.floor -= 1
        for item in self.items:
            item.floor = self.floor

    def embark(self, thing):
        if len(self.items) < capacity:
            self.items.append(thing)

    def debark(self):
        return self.items.pop()


class Chip:
    def __init__(self, type, floor):
        self.type = type
        self.gen = None
        self.floor = floor

    def attach(self, gen):
        if gen.type == self.type:
            self.gen = gen

    def detatch(self):
        self.gen = None


class Gen:
    def __init__(self, type, floor):
        self.type = type
        self.chip = None
        self.floor = floor

    def attach(self, chip):
        if chip.type == self.type:
            self.chip = gen

    def detatch(self):
        self.chip = None


class Floors(dict):
    def add(self, thing):
        ...
    

items = {
    'H-C': 1,
    'L-C': 1,
    'H-G': 2,
    'L-G': 3,
}

items = {
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
cur_floor = 1

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
    (Hand('PL-G', 'PR-G'), 1),
    (Hand('PL-G', 'PL-C'), 1),
    (Hand(None, 'PL-G'), -1),
    (Hand('PR-G', 'PL-G'), 1),
    (Hand(None, 'PR-G'), -1),
    (Hand(None, 'PR-G'), -1),
)

print('\n'*3)
print('\x1b[3A', end='')
print(floor_to_text(items), end='')
for move in moves:
    time.sleep(0.5)
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
    if all(items[item] == 4 for item in items):
        print('\nWon in {} steps!'.format(len(moves)))
