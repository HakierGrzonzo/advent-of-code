from sys import stdin
import numpy as np
from numpy.linalg import solve

data = stdin.read().strip().split("\n\n")

type Point = tuple[int, int]
#Point = "foo"

def parse_num_line(line: str)-> Point:
    _, _, x, y = line.split(" ")
    x = x.strip(',XY+')
    y = y.strip(',XY+')
    return int(x), int(y)

def parse_prize_line(line: str) -> Point:
    line = line.strip("Prize: ")
    prize = line.split(', ')
    return tuple([int(c.strip("XY=")) + 10000000000000 for c in prize])

def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])

def mul(a: Point, s: int) -> Point:
    return (a[0] * s, a[1] * s)

def diff(a: Point, b: Point) -> Point:
    return add(a, mul(b, -1))


acc = 0
for point in data:
    a_r, b_r, prize_r = point.split("\n")
    a = parse_num_line(a_r)
    b = parse_num_line(b_r)
    prize = parse_prize_line(prize_r)
    
    A = np.array([
        [a[0], b[0]],
        [a[1], b[1]]
    ])

    N = np.array(prize)
    solution = solve(A, N)
    a_mul, b_mul = solution

    integer_solution = np.array([round(a_mul), round(b_mul)])
    a_mul, b_mul = integer_solution

    location = add(mul(a, a_mul), mul(b, b_mul))
    is_correct = np.allclose(np.dot(A, integer_solution), N)
    if not is_correct: raise Exception("foo")
    if diff(location, prize) == (0, 0):
        acc += a_mul * 3 + b_mul






print(f"{acc=}")
        



