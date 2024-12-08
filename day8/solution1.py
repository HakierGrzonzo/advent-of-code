from sys import stdin
from collections import defaultdict
from itertools import product

data = stdin.readlines()

frequencies = defaultdict(lambda: list())

type Location = tuple[int, int]

for y, row in enumerate(data):
    for x, character in enumerate(row):
        if character == ".":
            continue
        frequencies[character].append((x, y))

def diff(a: Location, b: Location) -> Location:
    ax, ay = a
    bx, by = b
    return (ax - bx, ay - by)

def reverse(a: Location) -> Location:
    return -a[0], -a[1]

def add(a: Location, b: Location) -> Location:
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)

def eq(a: Location, b: Location) -> bool:
    ax, ay = a
    bx, by = b
    return all([ax == bx, ay == by])


def find_antinodes(locations: list[Location]):
    for a, b in product(locations, locations):

        offset = diff(a, b)
        if eq(offset, (0, 0)):
            continue

        candidates = []
        candidates.append(add(a, offset))
        candidates.append(add(b, offset))
        candidates.append(diff(a, offset))
        candidates.append(diff(b, offset))
        for c in candidates:
            if any([eq(c, i) for i in [a, b]]):
                continue
            yield c


grid = [list(r.strip()).copy() for r in data]
for character, locations in frequencies.items():
    print(character)
    for x, y in find_antinodes(locations):
        if x < 0 or y < 0:
            continue
        try:
            grid[y][x] = "#"
        except IndexError:
            pass
acc = 0
for row in grid:
    acc += row.count('#')
    print("".join(row))

print(acc)



