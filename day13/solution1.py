from sys import stdin

data = stdin.read().strip().split("\n\n")

type Point = tuple[int, int]

def parse_num_line(line: str)-> Point:
    _, _, x, y = line.split(" ")
    x = x.strip(',XY+')
    y = y.strip(',XY+')
    return int(x), int(y)

def parse_prize_line(line: str) -> Point:
    line = line.strip("Prize: ")
    prize = line.split(', ')
    return tuple([int(c.strip("XY=")) for c in prize])

def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])

def mul(a: Point, s: int) -> Point:
    return (a[0] * s, a[1] * s)


acc = 0
for point in data:
    a_r, b_r, prize_r = point.split("\n")
    a = parse_num_line(a_r)
    b = parse_num_line(b_r)
    prize = parse_prize_line(prize_r)
    print(f"{a=}, {b=}, {prize=}")
    max_a = max((prize[0] // a[0] + 1, prize[1] // a[1] + 1))
    a_count = max_a
    b_count = 0
    currentBestCost = float('inf')
    while a_count >= 0:
        location = add(mul(a, a_count), mul(b, b_count))
        cost = 3 * a_count + b_count
        if location[0] > prize[0] or location[1] > prize[1]:
            a_count -= 1
            continue
        elif location[0] == prize[0] and location[1] == prize[1]:
            currentBestCost = min(cost, currentBestCost)
            a_count -= 1
            continue
        else:
            b_count += 1
    if currentBestCost == float('inf'):
        print("NoCombination")
    else:
        print(currentBestCost)
        acc += currentBestCost

print(f"{acc=}")
        



