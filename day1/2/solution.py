from collections import defaultdict
from sys import stdin

data = stdin.readlines()

list_a, list_b = [], []

for line in data:
    a, b = line.split()
    list_a.append(int(a))
    list_b.append(int(b))

occurance_count = defaultdict(lambda: 0) 

for number in list_b:
    occurance_count[number] += 1

similiarity = 0

for number in list_a:
    similiarity += number * occurance_count.get(number, 0)

print(similiarity)
