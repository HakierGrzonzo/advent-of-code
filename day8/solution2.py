from sys import stdin
from collections import defaultdict
from itertools import product

data = stdin.readlines()

frequencies = defaultdict(lambda: list())

type Location = tuple[int, int]

for y, row in enumerate(data):
    for x, character in enumerate(row.strip()):
        if character == ".":
            continue
        frequencies[character].append((x, y))

def diff(a: Location, b: Location) -> Location:
    ax, ay = a
    bx, by = b
    return (ax - bx, ay - by)

def reverse(a: Location) -> Location:
    return -a[0], -a[1]

def l_abs(a: Location) -> Location:
    return abs(a[0]), abs(a[1])

def add(a: Location, b: Location) -> Location:
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)

def eq(a: Location, b: Location) -> bool:
    ax, ay = a
    bx, by = b
    return all([ax == bx, ay == by])

grid = [list(r.strip()).copy() for r in data]
max_y = len(grid)
max_x = len(grid[0])

def find_antinodes(locations: list[Location]):
    for a, b in product(locations, locations):
        print(a, b)

        offset = diff(a, b)
        if eq(offset, (0, 0)):
            continue
        
        yield b

        focus_point = b
        while True:
            nx, ny = diff(focus_point, offset)
            if nx > max_x or ny > max_y:
                break
            if nx < 0 or ny < 0:
                break
            yield nx, ny

            focus_point = (nx, ny)

        focus_point = b
        while True:
            nx, ny = add(focus_point, offset)
            if nx > max_x or ny > max_y:
                break
            if nx < 0 or ny < 0:
                break
            yield nx, ny
            focus_point = (nx, ny)




for character, locations in frequencies.items():
    print(character)
    for x, y in find_antinodes(locations):
        try:
            print(y, x)
            grid[y][x] = "#"
        except IndexError:
            continue
        """
        print("---")
        for row in grid:
            print("".join(row))
        print("---")
        """
acc = 0
for row in grid:
    acc += row.count('#')
    print("".join(row))

print(acc)



