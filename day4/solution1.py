from sys import stdin

data = stdin.read()

lines = data.splitlines(keepends=False)
rows = ["".join([line[n] for line in lines]) for n in range(len(lines[0]))]


def get_diagonal_asc(start_index):
    x = start_index
    y = 0
    acc = ""
    while True:
        try:
            acc += lines[x][::-1][y]
            x += 1
            y += 1
        except IndexError:
            break
    return acc

diagonals = []

MAX_LINE_LENGTH = len(lines[0])
MAX_ROW_LENGTH = len(lines)

for n in range(MAX_ROW_LENGTH):
    x = 0
    y = n
    acc = ""
    while x < MAX_LINE_LENGTH and y < MAX_ROW_LENGTH:
        acc += lines[y][x]
        y += 1
        x += 1
    diagonals.append(acc)

for n in range(MAX_ROW_LENGTH):
    x = n + 1
    y = 0
    acc = ""
    while x < MAX_LINE_LENGTH and y < MAX_ROW_LENGTH:
        acc += lines[y][x]
        x += 1
        y += 1
    diagonals.append(acc)

for n in range(MAX_ROW_LENGTH):
    x = MAX_LINE_LENGTH - 1
    y = n
    acc = ""
    while x >= 0 and y < MAX_ROW_LENGTH:
        acc += lines[y][x]
        y += 1
        x -= 1
    diagonals.append(acc)

for n in range(MAX_LINE_LENGTH):
    x = MAX_LINE_LENGTH - 2 - n
    y = 0
    acc = ""
    while x >= 0 and y >=0:
        acc += lines[y][x]
        x -= 1
        y += 1
    diagonals.append(acc)

candidate_set: list[str] = [
    *diagonals,
    *lines,
    *rows
]

acc = 0
for candidate in candidate_set:
    c1 = candidate.count("XMAS")
    c2 = candidate[::-1].count("XMAS")
    acc += c1 + c2
print(acc)

            
