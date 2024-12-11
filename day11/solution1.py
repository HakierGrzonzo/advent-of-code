stones = [int(stone) for stone in input().split(" ")]

for i in range(25):
    print(i, len(stones))
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif (stone_len := len(text_stone := str(stone))) % 2 == 0:
            stone_a = int(text_stone[:stone_len // 2])
            stone_b = int(text_stone[stone_len // 2:])
            new_stones.append(stone_a)
            new_stones.append(stone_b)
        else:
            new_stones.append(stone * 2024)
    stones = new_stones

print(len(stones))
