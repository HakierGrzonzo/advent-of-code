from sys import stdin

raw_patterns, raw_goals = stdin.read().strip().split('\n\n')

patterns = raw_patterns.split(', ')
goals = raw_goals.split('\n')

cache: dict[str, bool] = {}

def check(goal: str):
    is_maybe_possible = cache.get(goal)
    if is_maybe_possible is not None:
        return is_maybe_possible
    for pattern in [p for p in patterns if goal.startswith(p)]:
        if pattern == goal:
            return True
        if check(goal[len(pattern):]):
            cache[goal] = True
            return True
    cache[goal] = False
    return False

acc = 0
for goal in goals:
    res = check(goal)
    if res:
        acc+= 1
    print(f"{goal=}\t{res=}")

print(acc)
