import itertools
import time

SURROUNDING = set(itertools.permutations([0, 0, 1, 1, -1, -1], 2))
SURROUNDING = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
)

DEBUG = True

def is_wall(x, y, fave_number=1364):
    fnord = (x*x + 3*x + 2*x*y + y + y*y)+fave_number
    return bool('{:b}'.format(fnord).count('1') % 2)


def next_step(cur_x, cur_y, count=0, seen=set(), target=(31,39)):
    seen.add((cur_x, cur_y))
    possible = []
    for dx, dy in SURROUNDING:
        next_x = cur_x+dx
        next_y = cur_y+dy
        if (next_x, next_y) not in seen and not is_wall(next_x, next_y) and 0 <= next_x and 0 <= next_y:
            possible.append((cur_x, cur_y))
    return min(next_step(*step, count=count+1, seen=seen) for step in possible)


def find_shortest(x, y, target, seen, fave_number=10, count=0):
    if (x,y) == target:
        return count

    seen.add((x, y))
    possible = []
    for dx, dy in SURROUNDING:
        next_x, next_y = x+dx, y+dy
        if (next_x, next_y) not in seen and not is_wall(next_x, next_y, fave_number) and 0 <= next_x and 0 <= next_y:
            possible.append((next_x, next_y))

    results = [find_shortest(x=step[0], y=step[1], target=target, count=count+1, seen=seen, fave_number=fave_number)
               for step in possible]
    results = [result for result in results if result]
    if results:
        return min(results)
    return None
            

sample_maze = '''
.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###
'''.strip()

for y in range(7):
    print(''.join('#' if is_wall(x,y, fave_number=10) else '.' for x in range(10)))

maze = '\n'.join(''.join('#' if is_wall(x,y,10) else '.' for x in range(10))
                 for y in range(7))
MAP = maze
assert maze == sample_maze

test_shortest = find_shortest(1, 1, seen=set(), target=(7,4), fave_number=10)
assert test_shortest == 11

MAP = '\n'.join(''.join('#' if is_wall(x,y, 1364) else '.' for x in range(31))
                for y in range(39))

seen = set()
shortest = find_shortest(1, 1, seen=seen, target=(31,39), fave_number=1364)
print(shortest)

MAP = '\n'.join(''.join('#' if is_wall(x,y, 1364) else '.' if (x, y) not in seen else '\x1b[32mo\x1b[0m' for x in range(31))
                for y in range(39))
print(MAP)
print(seen)
