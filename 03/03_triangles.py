triangles = '''
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
'''.strip()


triangles = [[int(x) for x in triangle.split()] for triangle in triangles.split('\n')]


def is_valid_triangle(sides):
    longest = max(sides)
    rest = sum(side for side in sides if side != longest)
    return longest <= rest


real_triangles = []
for one, two, three in zip(*[iter(triangles)]*3):
    for i in range(3):
        real_triangles.append([one[i], two[i], three[i]])


#print(real_triangles)
count = 0
impossible = 0
for triangle in real_triangles:
    if is_valid_triangle(triangle):
        count += 1
    else:
        impossible += 1

print(count)
print(impossible)
print(count+impossible)

print()
count = 0
impossible = 0
for triangle in triangles:
    if is_valid_triangle(triangle):
        count += 1
    else:
        impossible += 1

print(count)
print(impossible)
print(count+impossible)
