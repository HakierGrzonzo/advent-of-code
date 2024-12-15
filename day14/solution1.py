from collections import defaultdict
from sys import stdin
from math import ceil, floor

data = stdin.read().strip().split('\n')

type Vector = tuple[int, int]
type Robot = tuple[Vector, Vector]

robots: list[Robot] = []

def parse_num(inp: str) -> Vector:
    inp = inp[2:]
    a, b = [int(n) for n in inp.split(',')]
    return a, b

for line in data:
    position, velocity = line.split(' ')
    position_x_y = parse_num(position)
    velocity_x_y = parse_num(velocity)
    robots.append((position_x_y, velocity_x_y))

"""
WIDTH = 11
HEIGHT = 7
"""
WIDTH = 101
HEIGHT = 103
TURNS = 100

robots_after: list[Vector] = []

for pos_x_y, vel_x_y in robots:
    x, y = [(p + v * TURNS) % limit for p, v, limit in zip(pos_x_y, vel_x_y, [WIDTH, HEIGHT])]
    robots_after.append((x, y))


positions_after = defaultdict(lambda: 0)
quadrants_after = defaultdict(lambda: 0)
mid_x = floor(WIDTH / 2) 
mid_y = floor(HEIGHT / 2)

for pos_x_y in robots_after:
    positions_after[pos_x_y] += 1
    x, y = pos_x_y
    if x == mid_x or y == mid_y:
        continue
    is_in_first_column = x < mid_x
    is_in_first_row = y < mid_y
    quadrants_after[(is_in_first_column, is_in_first_row)] += 1


def print_positions():
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if x == mid_x or y == mid_y:
                row += " "
                continue
            stat = positions_after[(x, y)]
            if stat == 0:
                row += "."
            else:
                row += str(stat)
        print(row)

print_positions()

ans = 1
for value in quadrants_after.values():
    ans *= value
print(ans)
                
