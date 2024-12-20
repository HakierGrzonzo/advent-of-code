from sys import stdin

raw_patterns, raw_goals = stdin.read().strip().split('\n\n')

patterns = raw_patterns.split(', ')
goals = raw_goals.split('\n')

cache: dict[str, int] = {}

def check(goal: str):
    acc = cache.get(goal)
    if acc is not None:
        return acc
    acc = 0
    for pattern in [p for p in patterns if goal.startswith(p)]:
        if pattern == goal:
            acc += 1
        else: 
            acc += check(goal[len(pattern):])
    cache[goal] = acc
    return acc

acc = 0
for goal in goals:
    acc += check(goal)
    print(f"{goal=}\t{acc=}")

print(acc)
