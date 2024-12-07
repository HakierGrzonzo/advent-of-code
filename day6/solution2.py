from sys import stdin
from time import sleep

data = stdin.read()
grid = [[*row] for row in data.split('\n')]

init_x = None
init_y = None

for x, row in enumerate(grid):
    for y, character in enumerate(row):
        if character == "^":
            init_x = x
            init_y = y
            break
    else:
        continue
    break
else:
    raise Exception("guard not found")

up = lambda x, y: (x-1, y)
up.__str__ = lambda: "↑"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "↓"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "←"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "→"
next_dir = {
    up: right,
    right: down,
    down: left,
    left: up
}


def is_loop(grid, debug = False):
    guard_direction = up
    x, y = init_x, init_y

    while True:
        if x < 0 or y < 0:
            return False
        grid[x][y] = guard_direction
        if debug:
            print_grid(grid, x, y)
        try:
            next_x, next_y = guard_direction(x, y)
            next_character = grid[next_x][next_y]
        except IndexError:
            break
        if next_character is guard_direction:
            return True
        while next_character in ["#", "O"]:
            guard_direction = next_dir[guard_direction]
            next_x, next_y = guard_direction(x, y)
            if next_x < 0 or next_y < 0:
                return False
            try:
                next_character = grid[next_x][next_y]
            except IndexError:
                return False
        x, y = next_x, next_y
    return False

def print_grid(grid, x = None, y=None):
    if x is not None and y is not None:
        new_grid = [row.copy() for row in grid.copy()]
        new_grid[x][y] = "@"
    else:
        new_grid = grid
    for row in new_grid:
        print("".join(r.__str__() for r in row))

acc = 0
for x, row in enumerate(grid):
    for y, character in enumerate(row):
        print(x, y, acc)
        if x == 112 and y == 50:
            acc += 1
            continue
        if character == "^" or character == "#":
            continue
        new_grid = [row.copy() for row in grid.copy()]
        new_grid[x][y] = "O"
        if is_loop(new_grid):
            acc += 1
print(acc)
