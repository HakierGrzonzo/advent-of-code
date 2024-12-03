from sys import stdin
from itertools import pairwise

data = stdin.readlines()

reports = [[int(n) for n in line.split(" ")] for line in data]

result = 0
for report in reports:
    diffs = [a - b for a, b in pairwise(report)]
    is_direction_consistant = all(d > 0 for d in diffs) or all(d < 0 for d in diffs)
    is_growth_normal = all(1 <= abs(d) <= 3 for d in diffs)
    safe = is_direction_consistant and is_growth_normal 
    #print(f"{'safe' if safe else 'unsafe'}\t{repr(report)}\t{is_direction_consistant=} {is_growth_normal=}")

    if safe:
        result += 1
print(result)

