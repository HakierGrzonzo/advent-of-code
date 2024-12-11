from collections import defaultdict
from multiprocessing import Pool

stones = [int(stone) for stone in input().split(" ")]

cache = defaultdict(lambda: dict())

target = 75

def do_step(stone: int, depth: int = 1):
    cached_solution = cache[stone].get(depth)
    if cached_solution:
        return cached_solution
    if depth > target:
        result = 1 
    elif stone == 0:
        result = do_step(1, depth + 1)
    elif (stone_len := len(text_stone := str(stone))) % 2 == 0:
        stone_a = int(text_stone[:stone_len // 2])
        stone_b = int(text_stone[stone_len // 2:])
        result = do_step(stone_a, depth + 1) + do_step(stone_b, depth + 1)
    else:
        result = do_step(stone * 2024, depth + 1)
    cache[stone][depth] = result
    return result

"""
with Pool(processes=24) as pool:
    results = pool.imap_unordered(do_step, stones, chunksize=16)
    acc = 0
    for index, result in enumerate(results):
        print(f"{round((index / len(stones)) * 100_000) / 100 }%")
        acc += result
"""
acc = 0
for index, stone in enumerate(stones):
    acc += do_step(stone)
    print(f"{index}/{len(stones)}")
print(acc)

print(sum(len(v.values()) for v in cache.values()))

