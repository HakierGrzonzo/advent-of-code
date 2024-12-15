from sys import stdin
from itertools import pairwise

data = stdin.read().split('\n')

grid: dict[int, dict[int, str]] = {y: {x: cell for x, cell in enumerate(row)} for y, row in enumerate(data)}

already_visited = []

up = lambda x, y: (x-1, y)
up.__str__ = lambda: "↑"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "↓"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "←"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "→"

movements = [up, left, right, down]
def walk_region(y: int, x: int, target: str):
    cell = grid.get(y, {}).get(x)
    if cell == None or (y, x) in already_visited or cell != target:
        yield from []
        return
    yield (y, x)
    already_visited.append((y, x))
    for direction in movements:
        yield from walk_region(*direction(y, x), target)

regions: list[tuple[str, list[tuple[int, int]]]] = []

for y, row in grid.items():
    for x, cell in row.items():
        region = list(walk_region(y, x, cell))
        if len(region) > 0:
            regions.append((cell, region))

def calculate_permieter(region_locations: list[tuple[int, int]]):
    perimeter = 0
    for y, x in region_locations:
        for direction in movements:
            new_y, new_x = direction(y, x)
            if (new_y, new_x) not in region_locations:
                perimeter += 1

    return perimeter

def number_of_fragments(locations: list[tuple[int, int]], horizontal: bool):
    if len(locations) == 0:
        return 0
    acc = 1
    locations = sorted(locations, key=lambda loc: (loc[1] if horizontal else loc[0]))
    for (y1, x1), (y2, x2) in pairwise(locations):
        if abs(x1 - x2) > 1 and horizontal:
            acc += 1
        elif abs(y1 - y2) > 1:
            acc += 1
    return acc

def calculate_fences(region_locations: list[tuple[int, int]]):
    min_y = min(y for y, _ in region_locations)
    max_y = max(y for y, _ in region_locations)
    vertical_fences = 0
    for y in range(min_y, max_y + 1):
        for direction in [up, down]:
            cells = [cell for cell in region_locations if cell[0] == y and direction(*cell) not in region_locations]
            vertical_fences += number_of_fragments(cells, horizontal=True)

    min_x = min(x for _, x in region_locations)
    max_x = max(x for _, x in region_locations)
    horizontal_fences = 0
    for x in range(min_x, max_x+ 1):
        for direction in [left, right]:
            cells = [cell for cell in region_locations if cell[1] == x and direction(*cell) not in region_locations]
            horizontal_fences += number_of_fragments(cells, horizontal=False)
    return vertical_fences + horizontal_fences

price = 0

for region_kind, locations in regions:
    area = len(locations)
    permieter = calculate_fences(locations)
    cost = permieter * area
    print(f'{region_kind}: {area=} * {permieter=}\t= {cost=}')
    price += cost 

print(f"{price=}")

