from collections import defaultdict
from sys import stdin
from typing import Callable

board, moves = stdin.read().strip().split('\n\n')

grid: dict[int, dict[int, str]] = defaultdict(lambda: {})

robot: tuple[int, int] = None

for y, row in enumerate(board.split('\n')):
    for x, char in enumerate(row):
        grid[y][x] = char
        if char == "@":
            print("found robot")
            robot = (y, x)

up = lambda x, y: (x-1, y)
up.__str__ = lambda: "↑"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "↓"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "←"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "→"

movements = {
    '>': right,
    '<': left,
    '^': up,
    'v': down
}

def print_grid():
    rows = sorted([(k, row) for k, row in grid.items()], key=lambda e: e[0])
    out = []
    for _, row in rows:
        chars = sorted([(k, c) for k, c in row.items()], key=lambda e: e[0])
        line = ""
        for _, c in chars:
            line += c
        out.append(line)
    print("\n".join(out))

def try_move_crate(y: int, x: int, direction: Callable[[int, int], tuple[int, int]]):
    char_at_pos = grid[y][x]
    assert char_at_pos == "O"
    new_y, new_x = direction(y, x)
    char_to_move_to = grid[new_y][new_x]
    if char_to_move_to == ".":
        grid[y][x], grid[new_y][new_x] = grid[new_y][new_x], grid[y][x]
        return True
    elif char_to_move_to == "#":
        return False
    else:
        assert char_to_move_to == "O"
        if try_move_crate(new_y, new_x, direction):
            assert grid[new_y][new_x] == "."
            grid[y][x], grid[new_y][new_x] = grid[new_y][new_x], grid[y][x]
            return True
        else:
            return False






for move in moves:
    if move == "\n":
        continue
    func = movements[move]
    y, x = robot
    new_y, new_x = func(*robot)
    char_at_pos = grid[new_y][new_x]
    if char_at_pos == "#":
        continue
    elif char_at_pos == ".":
        grid[y][x], grid[new_y][new_x] = grid[new_y][new_x], grid[y][x]
        robot = (new_y, new_x)
    else:
        assert char_at_pos == "O"
        if try_move_crate(new_y, new_x, func):
            grid[y][x], grid[new_y][new_x] = grid[new_y][new_x], grid[y][x]
            robot = (new_y, new_x)
        else:
            continue

print_grid()

acc = 0
rows = sorted([(k, row) for k, row in grid.items()], key=lambda e: e[0])
out = []
for y, row in rows:
    chars = sorted([(k, c) for k, c in row.items()], key=lambda e: e[0])
    for x, c in chars:
        if c == "O":
            acc += 100 * y + x
print(f"{acc=}")




