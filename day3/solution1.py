from sys import stdin
import re

data = stdin.read()

regex = re.compile(r"mul\((\d+),(\d+)\)")

results = re.findall(regex, data)

acc = 0
for a, b in results:
    acc += int(a) * int(b)

print(acc)
