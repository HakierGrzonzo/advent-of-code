from sys import stdin
import re

data = stdin.read()

regex = re.compile(r"(?P<mul>mul\((\d+),(\d+)\))|(?P<do>do\(\))|(?P<dont>don't\(\))")

results = re.findall(regex, data)

acc = 0
mul_enable = True
for mul, a, b, do, dont in results:
    if mul and mul_enable:
        acc += int(a) * int(b)
    if do:
        mul_enable = True
    if dont:
        mul_enable = False


print(acc)
