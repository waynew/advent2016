from enum import Enum

class Direction(Enum):
    north = (0, 1)
    east = (1, 0)
    south = (0, -1)
    west = (-1, 0)

    def turn(self, turn):
        assert turn in ('L', 'R')

        if turn == 'L':
            new_directions = {
                Direction.north: Direction.west,
                Direction.west: Direction.south,
                Direction.south: Direction.east,
                Direction.east: Direction.north,
            }
        elif turn == 'R':
            new_directions = {
                Direction.north: Direction.east,
                Direction.east: Direction.south,
                Direction.south: Direction.west,
                Direction.west: Direction.north,
            }

        return new_directions[self]


direction = Direction.north
position = [0, 0]
visited = set()

steps = 'L1, R3, R1, L5, L2, L5, R4, L2, R2, R2, L2, R1, L5, R3, L4, L1, L2, R3, R5, L2, R5, L1, R2, L5, R4, R2, R2, L1, L1, R1, L3, L1, R1, L3, R5, R3, R3, L4, R4, L2, L4, R1, R1, L193, R2, L1, R54, R1, L1, R71, L4, R3, R191, R3, R2, L4, R3, R2, L2, L4, L5, R4, R1, L2, L2, L3, L2, L1, R4, R1, R5, R3, L5, R3, R4, L2, R3, L1, L3, L3, L5, L1, L3, L3, L1, R3, L3, L2, R1, L3, L1, R5, R4, R3, R2, R3, L1, L2, R4, L3, R1, L1, L1, R5, R2, R4, R5, L1, L1, R1, L2, L4, R3, L1, L3, R5, R4, R3, R3, L2, R2, L1, R4, R2, L3, L4, L2, R2, R2, L4, R3, R5, L2, R2, R4, R5, L2, L3, L2, R5, L4, L2, R3, L5, R2, L1, R1, R3, R3, L5, L2, L2, R5'.split(', ')

for count, step in enumerate(steps):
    turn = step[0]
    distance = int(step[1:])
    direction = direction.turn(turn)
    position[0] += direction.value[0]*distance
    position[1] += direction.value[1]*distance
    pos = tuple(position)
    if pos in visited:
        print(pos, step, count)
        print(sum(abs(x) for x in pos))
        break
    visited.add(pos)
