from collections import defaultdict
from sys import stdin
from typing import Callable

board, moves = stdin.read().strip().split('\n\n')

grid: dict[int, dict[int, str]] = defaultdict(lambda: {})

robot: tuple[int, int] = None

for y, row in enumerate(board.split('\n')):
    for x, char in enumerate(row):
        if char == "O":
            grid[y][2 * x] = "["
            grid[y][2 * x + 1] = "]"
        elif char == "@":
            print("found robot")
            robot = (y, 2* x)
            grid[y][2 * x] = char
            grid[y][2 * x + 1] = "."
        else:
            grid[y][2 * x] = char
            grid[y][2 * x + 1] = char

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

def can_move_crate(y: int, x: int, direction: Callable[[int, int], tuple[int, int]]):
    char_at_pos = grid[y][x]
    if char_at_pos == ".": 
        return True
    if char_at_pos == "#":
        return False
    if char_at_pos == "]":
        x -= 1
    char_at_pos = grid[y][x]
    assert char_at_pos == "["
    assert grid[y][x+1] == "]"
    positions = [direction(y, x), direction(y, x + 1)]
    return all(can_move_crate(*p, direction) for p in positions)

def move_crate(y: int, x: int, direction: Callable[[int, int], tuple[int, int]]):
    char_at_pos = grid[y][x]
    if char_at_pos == ".": 
        return 
    if char_at_pos == "#":
        raise Exception("not crate")
    if char_at_pos == "]":
        x -= 1
    char_at_pos = grid[y][x]
    assert char_at_pos == "["
    assert grid[y][x+1] == "]"
    positions = [direction(y, x), direction(y, x + 1)]
    for position in positions:
        move_crate(*position, direction)
    assert all(grid[p_y][p_x] == "." for p_y, p_x in positions)
    grid[y][x] = "."
    grid[y][x + 1] = "."
    next_y, next_x = direction(y, x)
    grid[next_y][next_x] = "["
    grid[next_y][next_x + 1] = "]"



def try_move_crate(y: int, x: int, direction: Callable[[int, int], tuple[int, int]]):
    char_at_pos = grid[y][x]
    if char_at_pos == ".":
        return True
    if char_at_pos == "#":
        return False
    if direction is left:
        assert char_at_pos == "]"
        l_y, l_x = direction(y, x)
        second_part_of_box = grid[l_y][l_x]
        assert second_part_of_box == "["
        ll_y, ll_x = direction(l_y, l_x)
        if try_move_crate(ll_y, ll_x, direction):
            grid[ll_y][ll_x], grid[l_y][l_x], grid[y][x] = "[]."
            return True
        return False
    elif direction is right:
        assert char_at_pos == "["
        l_y, l_x = direction(y, x)
        second_part_of_box = grid[l_y][l_x]
        assert second_part_of_box == "]"
        ll_y, ll_x = direction(l_y, l_x)
        if try_move_crate(ll_y, ll_x, direction):
            grid[y][x], grid[l_y][l_x], grid[ll_y][ll_x] = ".[]"
            return True
        return False
    elif direction is up or direction is down:
        if not can_move_crate(y, x, direction):
            return False
        move_crate(y, x, direction)
        return True
    else:
        raise Exception("foo")

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
        assert char_at_pos in ["[", "]"]
        if try_move_crate(new_y, new_x, func):
            grid[y][x] = "."
            grid[new_y][new_x] = "@"
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
        if c == "[":
            acc += 100 * y + x
print(f"{acc=}")




