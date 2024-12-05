from sys import stdin

lines = stdin.read().splitlines(keepends=False)

def is_x_mas(x: int, y: int):
    conditions = [
        lines[x+1][y+1] == "A",
        (lines[x][y] == "M" and lines[x + 2][y + 2] == "S") or (
         lines[x][y] == "S" and lines[x + 2][y + 2] == "M"
        ),
        (lines[x][y + 2] == "M" and lines[x + 2][y] == "S") or (
         lines[x][y + 2] == "S" and lines[x + 2][y] == "M"
        )
    ]
    return all(conditions)

acc = 0

for x in range(len(lines)):
    for y in range(len(lines[0])):
        try:
            acc += is_x_mas(x, y)
        except IndexError:
            pass

print(acc)

