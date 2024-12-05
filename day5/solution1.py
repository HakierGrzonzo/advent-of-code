from sys import stdin
from collections import defaultdict

data = stdin.read()

header, candidates = data.split("\n\n")

header_rules = [row.split('|') for row in header.split("\n")]

header_rule_dict = defaultdict(lambda: list())
for a, b in header_rules:
    header_rule_dict[int(b)].append(int(a))

candidates = candidates.strip().split('\n')
candidates = [[int(x) for x in c.split(",")] for c in candidates]

def validate_order(c: list[int]):
    for index, number in enumerate(c):
        must_have_pages = header_rule_dict[number]
        if all(page in c[:index] or page not in c for page in must_have_pages):
            continue
        else:
            return False
    return True

acc = 0
for c in candidates:
    if validate_order(c):
        middle = (len(c) - 1)  // 2
        acc += c[middle]
print(acc)
