from sys import stdin
from operator import __add__, __mul__

lines = stdin.readlines()

acc = 0


def try_get_result(target: int, nums: list[int]):
    if len(nums) == 1:
        return nums[0] == target
    operators = [__add__, __mul__]
    for operator in operators:
        a, b, *rest = nums
        new_num = operator(a, b)
        new_nums = [new_num, *rest]
        if try_get_result(target, new_nums):
            return True
    else:
        return False

for line in lines:
    target, nums = line.split(': ')
    target = int(target)
    nums = [int(n) for n in nums.split(' ')]
    if try_get_result(target, nums):
        acc += target
print(acc)
