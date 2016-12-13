import itertools
import time
from collections import namedtuple

SURROUNDING = set(itertools.permutations([0, 0, 1, 1, -1, -1], 2))
SURROUNDING = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
)

DEBUG = True

class Node:
    def __init__(self, x, y, neighbors=None):
        self.x = x
        self.y = y
        self.dist = None
        self.neighbors = neighbors or []

def is_wall(x, y, fave_number=1364):
    fnord = (x*x + 3*x + 2*x*y + y + y*y)+fave_number
    return bool('{:b}'.format(fnord).count('1') % 2)


def surrounding_nodes(x, y, fave_number):
    nodes = []
    for dx, dy in SURROUNDING:
        next_x, next_y = x+dx, y+dy
        if 0 <= next_x and 0 <= next_y and not is_wall(next_x, next_y, fave_number):
            nodes.append((next_x, next_y))
    return nodes


def build_graph(start_x, start_y, target, fave_number):
    graph = {
        (start_x, start_y): {'neighbors': [], 'dist': 0}
    }
    unvisited = set()
    cur = list(graph)[0]
    while cur != target:
        graph[cur]['neighbors'] = surrounding_nodes(cur[0], cur[1], fave_number)
        for node in graph[cur]['neighbors']:
            if node not in graph:
                graph[node] = {'neighbors': [], 'dist': None}
                graph[node]['dist'] = graph[cur]['dist']
                unvisited.add(node)
        cur = unvisited.pop()


    real_graph = {}
    for coord in graph:
        real_graph[coord] = Node(coord[0], coord[1], neighbors=graph[coord]['neighbors'])

    cur = (start_x, start_y)
    start = real_graph[cur]
    cur_node = start
    next_node = None
    start.dist = 0
    while cur != target:
        for neighbor in cur_node.neighbors:
            if neighbor.dist is None:
                neighbor.dist = cur_node.dist+1
            else:
                neighbor.dist = min(cur_node.dist+1, neighbor.dist)
        for neighbor in cur_node.neighbors:
            if next_node is None or neighbor.dist < next_node.dist:
                next_node = neighbor
        if next_node is None:
            next_node = real_graph.pop(list(real_graph)[0])
        cur = (next_node.x, next_node_y)
        cur_node = next_node

    print(target.dist)



sample_maze = '''
.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###
'''.strip()

#test_shortest = find_shortest(1, 1, seen=set(), target=(7,4), fave_number=10)

build_graph(1,1, (7,4), fave_number=10)
