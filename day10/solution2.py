from sys import stdin

grid = [[int(n) if n != "." else None for n in row] for row in stdin.read().split('\n')]


up = lambda x, y: (x-1, y)
up.__str__ = lambda: "↑"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "↓"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "←"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "→"

movements = [up, left, right, down]


def walk_trail(x: int, y: int, state = 0):
    current_square = grid[x][y]
    if current_square == 9:
        yield (x, y)
    if current_square != state:
        raise Exception("wrong state?")
    for direction in movements:
        next_x, next_y = direction(x, y)
        if next_x < 0 or next_y < 0:
            continue
        try:
            next_square = grid[next_x][next_y]
        except IndexError:
            continue
        if next_square != state + 1:
            continue
        yield from walk_trail(next_x, next_y, state + 1)


acc = 0

for x, row in enumerate(grid):
    for y, char in enumerate(row):
        if char != 0:
            continue
        points_reachable = list()
        for point in walk_trail(x, y):
            points_reachable.append(point)
        acc += len(points_reachable)


print(acc)

