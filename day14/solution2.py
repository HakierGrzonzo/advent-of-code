from collections import defaultdict
from sys import stdin
from itertools import count
from math import floor
from statistics import mean

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

x_variance = []
y_variance = []

for t in range(10_000):
    print(t, end="\r")
    robots_after: list[Vector] = []

    for pos_x_y, vel_x_y in robots:
        x, y = [(p + v * t) % limit for p, v, limit in zip(pos_x_y, vel_x_y, [WIDTH, HEIGHT])]
        robots_after.append((x, y))

    positions_after = defaultdict(lambda: 0)

    for pos_x_y in robots_after:
        positions_after[pos_x_y] += 1
        x, y = pos_x_y

    mean_x = mean(x for x, _ in robots_after)
    mean_y = mean(y for _, y in robots_after)
    
    variance_x = sum((x - mean_x) ** 2 for x, _ in robots_after) / len(robots_after)
    variance_y = sum((y - mean_y) ** 2 for _, y in robots_after) / len(robots_after)
    x_variance.append(variance_x)
    y_variance.append(variance_y)

    def print_positions():
        out = []
        for y in range(HEIGHT):
            row = ""
            for x in range(WIDTH):
                stat = positions_after[(x, y)]
                if stat == 0:
                    row += "."
                else:
                    row += str(stat)
            out.append(row)
        print("\033[2J")
        print("\n".join(out))

    if variance_x < 400 and variance_y < 400:
        print_positions()
        print(t)
        breakpoint()




print(f"{mean(x_variance)=}, {min(x_variance)=}, {mean(y_variance)=}, {min(y_variance)=}")
