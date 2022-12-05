import re
from typing import Tuple

Interval = Tuple[int, int]


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def is_in(val: int, interval: Interval) -> bool:
    return interval[0] <= val <= interval[1]


def is_included(interval1: Interval, interval2: Interval) -> bool:
    return is_in(interval1[0], interval2) and is_in(interval1[1], interval2)


def overlaps(interval1: Interval, interval2: Interval) -> bool:
    return is_in(interval1[0], interval2) or \
           is_in(interval1[1], interval2) or \
           is_in(interval2[0], interval1)


def task1(inp: str) -> int:
    lines = inp.split()
    count = 0
    for line in lines:
        match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        nums = list(map(int, match.groups()))
        interval1 = (nums[0], nums[1])
        interval2 = (nums[2], nums[3])
        if is_included(interval1, interval2) or is_included(interval2, interval1):
            count += 1
    return count


def task2(inp) -> int:
    lines = inp.split()
    count = 0
    for line in lines:
        match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        nums = list(map(int, match.groups()))
        interval1 = (nums[0], nums[1])
        interval2 = (nums[2], nums[3])
        if overlaps(interval1, interval2):
            count += 1
    return count


text = fts("04in.txt")
print(task1(text))
print(task2(text))

