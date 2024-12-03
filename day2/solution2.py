from sys import stdin
from itertools import pairwise

data = stdin.readlines()

reports = [[int(n) for n in line.split(" ")] for line in data]

def is_report_safe(report: list[int]):
    diffs = [a - b for a, b in pairwise(report)]
    is_direction_consistant = all(d > 0 for d in diffs) or all(d < 0 for d in diffs)
    is_growth_normal = all(1 <= abs(d) <= 3 for d in diffs)
    safe = is_direction_consistant and is_growth_normal 
    return safe

result = 0
for report in reports:
    safe = is_report_safe(report)
    if not safe:
        for n in range(len(report)):
            new_report = report[:n] + report[n + 1:]
            safe = is_report_safe(new_report)
            if safe:
                break
    #print(f"{'safe' if safe else 'unsafe'}\t{repr(report)}")

    if safe:
        result += 1
print(result)

