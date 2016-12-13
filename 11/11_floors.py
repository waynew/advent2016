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

items = {
    'PL-G': 1,
    'TH-G': 1,
    'TH-C': 1,
    'PR-G': 1,
    'RU-G': 1,
    'RU-C': 1,
    'CO-G': 1,
    'CO-C': 1,
    'PL-C': 1,
    'PR-C': 1,
}

target = {
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


def floor_to_text(floors, cur_floor=1):
    text = []
    all_items = sum(floors, ())
    for floor_num, floor in enumerate(floors, start=1):
        if floor_num == cur_floor:
            elevator = '\x1b[;41m{}\x1b[0m'.format(floor_num)
        else:
            elevator = floor_num
        thing = ' '.join('{: ^{}}'.format((item if item in floor else '.'), len(all_items[0])) for item in all_items)
        text.insert(0, '{} {}'.format(elevator, thing))

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


def fried(floors):
    for floor in floors:
        for chip in (chip for chip in floor if chip.endswith('-C')):
            if chip.replace('-C', '-G') not in floor and any(thing.endswith('-G') for thing in floor):
                return True


def to_dict(floors):
    items = {}
    for num, floor in enumerate(floors, 1):
        for item in floor:
            items[item] = num
    return items


def to_tuple(items):
    floors = []
    for i in range(4):
        floor_num = i+1
        floors.append(tuple(sorted(item for item in items if items[item] == floor_num)))
    return tuple(floors)


def possible_moves(item, floors, floor_limit=4):
    items = to_dict(floors)
    elevator = items[item]
    moves = []

    other_items = [i for i in items if i != item and items[item] == items[i]]

    next_floors = []
    if elevator < floor_limit:
        next_floors.append(elevator+1)
    if elevator > 1:
        next_floors.append(elevator-1)

    for next_floor in next_floors:
        for paired_item in other_items:
            if items[paired_item] == items[item]:
                items[paired_item] = next_floor
                items[item] = next_floor
                moves.append((next_floor, to_tuple(items)))
                items[paired_item] = elevator
                items[item] = elevator
            items[item] = next_floor
            moves.append((next_floor, to_tuple(items)))
            items[item] = elevator

    moves = [move for move in moves if not fried(move[1])]
    return moves


Move = namedtuple('Move', ('from_', 'to'))


def find_shortest(floors, elevator=1, steps=0, seen=None):
    start = (elevator, floors)
    states = {
        (elevator, floors): set(sum((possible_moves(item, floors, floor_limit=4) for item in floors[elevator-1]), []))
    }
    traversed_edges = set()
    for dest in states[(elevator, floors)]:
        states[dest] = None
        traversed_edges.add(Move(from_=(elevator, floors), to=dest))
        
    while any(states[state] is None for state in states):
        state = next(state for state in states if states[state] is None)
        state_floor = state[0]-1
        states[state] = states.get(state) or set()
        for item in state[1][state_floor]:
            for move in possible_moves(item, state[1], floor_limit=4):
                states[state].add(move)
                transition = Move(from_=state, to=move)
                traversed_edges.add(transition)
                states[move] = states.get(move, None)

    distances = {state:float('inf') for state in states}
    distances[start] = 0
    unvisited = set(distances)

    while unvisited:
        current = min((distances[state], state) for state in unvisited)[1] 
        unvisited.remove(current)
        dist = distances[current]+1
        for neighbor in states[current]:
            distances[neighbor] = min(distances[neighbor], dist)

    for thing in distances:
        if not any(thing[1][:3]):
            print(thing)
    return distances


if __name__ == '__main__':
    target = (
        (),
        (),
        (),
        ('PL-G', 'TH-G', 'TH-C', 'PR-G', 'RU-G',
         'RU-C', 'CO-G', 'CO-C', 'PL-C', 'PR-C',
         ),
    )
    assert fried([['H-C', 'F-G'],])
    assert not fried((['H-C', 'H-G'],))
    assert fried((['H-C', 'H-G', 'F-C'],))
    assert not fried((['H-C', 'H-G', 'F-C', 'F-G'],))
    assert not fried((['H-G',  'F-G'], ['H-C', 'F-C']))


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
    target = {
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

    initial_state = (
        ('H-C', 'L-C'),
        ('H-G',),
        ('L-G',),
        (),
    )
    target = (
        (), (), (),
        tuple(sorted(('H-C', 'L-C', 'H-G', 'L-G')))
    )

    assert to_dict(initial_state) == to_dict(initial_state)
    assert to_tuple(to_dict(initial_state)) == initial_state

    valid_moves_hc = [
        (2, (('L-C',),
             ('H-C', 'H-G'),
             ('L-G',),
             (),
             )
         ),
    ]
    assert possible_moves('H-C', initial_state, floor_limit=4) == valid_moves_hc
    assert possible_moves('L-C', initial_state, floor_limit=4) == []

    assert possible_moves('H-G', (('L-C',), ('H-C', 'H-G'), ('L-G',), ())) == [(3, (('L-C',), (), ('H-C', 'H-G', 'L-G'), ())),
                                                                               (3, (('L-C',), ('H-C',), ('H-G', 'L-G'), ())),
                                                                               ]

    initial_state = (
        ('H-C', 'L-C'),
        ('H-G',),
        ('L-G',),
        (),
    )
    target = (4, (
        (), (), (),
        tuple(sorted(('H-C', 'L-C', 'H-G', 'L-G')))
    ))

    print(find_shortest(initial_state, elevator=1)[target]-2)

    initial_state = (
        ('PL-G',
         'TH-G',
         'TH-C',
         'PR-G',
         'RU-G',
         'RU-C',
         'CO-G',
         'CO-C',
         ),
        ('PL-C',
         'PR-C',
         ),
         (),(),
    )
    target = (4, ((), (), (),
                  ('PL-G', 'TH-G', 'TH-C', 'PR-G', 'RU-G',
                   'RU-C', 'CO-G', 'CO-C', 'PL-C', 'PR-C',
                   )))
    print(find_shortest(initial_state, elevator=1)[target]-2)
