import itertools
import time
from collections import namedtuple

SURROUNDING = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
)

Coord = namedtuple('Coord', 'x,y')

def is_wall(x, y, fave_number=1364):
    fnord = (x*x + 3*x + 2*x*y + y + y*y)+fave_number
    return bool('{:b}'.format(fnord).count('1') % 2)


def surrounding_nodes(x, y, fave_number):
    nodes = []
    for dx, dy in SURROUNDING:
        next_x, next_y = x+dx, y+dy
        if 0 <= next_x and 0 <= next_y and not is_wall(next_x, next_y, fave_number):
            nodes.append(Coord(next_x, next_y))
    return nodes


def build_graph(start_x, start_y, target, fave_number):
    start = Coord(start_x, start_y)
    distances = {
    }
    graph = {
        start: {'neighbors': [], 'dist': 0}
    }
    unvisited = set()
    cur = list(graph)[0]
    while cur != target:
        graph[cur]['neighbors'] = surrounding_nodes(cur.x, cur.y, fave_number)
        for coord in graph[cur]['neighbors']:
            if coord not in graph:
                graph[coord] = {'neighbors': [], 'dist': None}
                unvisited.add(coord)
        cur = unvisited.pop()
    distances[start] = 0

    unvisited = set(graph)
    for coord in unvisited:
        distances[coord] = distances.get(coord, float('inf'))

    while unvisited:
        current = min((distances[coord], coord) for coord in unvisited)[1]
        unvisited.remove(current)
        dist = distances[current]+1

        for neighbor in graph[current]['neighbors']:
            distances[neighbor] = min(distances[neighbor], dist)
    return distances


assert 11 == build_graph(1,1, (7,4), fave_number=10)[(7,4)]
graph = build_graph(1,1, (31,39), fave_number=1364) 
print(graph[(31,39)])
print(sum(1 for g in graph if graph[g] <= 50))
