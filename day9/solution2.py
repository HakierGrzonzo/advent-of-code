from sys import stdin
from itertools import count

data = iter(stdin.read().strip())

disk_map = []
counter = count(0)

def get_block_index_with_size(size: int):
    for index, (block_size, block_type) in enumerate(disk_map):
        if block_size >= size and block_type == ".":
            return index
    else:
        return None

while True:
    try:
        file_size = int(next(data))
    except StopIteration:
        break
    file_id = next(counter)
    disk_map.append((file_size, file_id))

    try:
        free_space = int(next(data))
    except StopIteration:
        break
    disk_map.append((free_space, '.'))

def debug_disk_map(map):
    raw_disk = []
    for size, block_id in map:
        for _ in range(size):
            raw_disk.append(block_id)
    print("".join(str(n) for n in raw_disk))

def map_index_to_raw(index: int):
    acc = 0
    for _ in range(index):
        block_size, _ = disk_map[index]
        acc += block_size
    return acc



for index in reversed(range(len(disk_map))):
    size, block_id = disk_map[index]
    if block_id == ".":
        continue
    first_free_index = get_block_index_with_size(size)
    if first_free_index is None or first_free_index >= index:
        continue

    free_blocks, _ = disk_map[first_free_index]
    if free_blocks == size:
        disk_map[index], disk_map[first_free_index] = disk_map[first_free_index], disk_map[index]
    else:
        disk_map[index] = (size, ".")
        disk_map = disk_map[:first_free_index] + [(size, block_id), (free_blocks - size, ".")] + disk_map[first_free_index+1:]



raw_disk = []
for size, block_id in disk_map:
    for _ in range(size):
        raw_disk.append(block_id)

check_sum = 0
for index, char in enumerate(raw_disk):
    if char == ".":
        continue
    check_sum += char * index


print("".join(str(n) for n in raw_disk), check_sum)
