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

def has_dependencies_satisfied(number: int, before: list[int], whole_list: list[int]):
    must_have_pages = header_rule_dict[number]
    return all(page in before or page not in whole_list for page in must_have_pages)


def sort_order(c: list[int]):
    while not validate_order(c):
        for i in range(len(c)):
            current = c[i]
            before = c[:i]
            if has_dependencies_satisfied(current, before, c):
                continue
            next_num = c[i + 1]
            c[i], c[i+1] = next_num, current
    return c


acc = 0
for c in candidates:
    if validate_order(c):
        continue
    c = sort_order(c)
    middle = (len(c) - 1)  // 2
    acc += c[middle]

print(acc)
