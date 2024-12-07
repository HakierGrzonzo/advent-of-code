from sys import stdin

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
down = lambda x, y: (x+1, y)
left = lambda x, y: (x, y-1)
right = lambda x, y: (x, y+1)

next_dir = {
    up: right,
    right: down,
    down: left,
    left: up
}

guard_direction = up

x, y = init_x, init_y

while True:
    grid[x][y] = "X"
    try:
        next_x, next_y = guard_direction(x, y)
        next_character = grid[next_x][next_y]
    except IndexError:
        print(x, y)
        break
    if next_character == "#":
        guard_direction = next_dir[guard_direction]
        continue
    x, y = next_x, next_y

acc = 0
for row in grid:
    print("".join(row))
    for character in row:
        if character == "X":
            acc += 1

print(acc)
