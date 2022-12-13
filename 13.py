from typing import Union, List

Value = Union[int, List['Value']]


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def cmp(left: Value, right: Value) -> int:
    if type(left) == type(right) == int:
        if left < right:
            return 1
        if left > right:
            return -1
        return 0

    if type(left) == int:
        left = [left]

    if type(right) == int:
        right = [right]

    for i in range(min(len(left), len(right))):
        c = cmp(left[i], right[i])
        if c != 0:
            return c
    if (len(left)) > len(right):
        return -1
    if (len(left)) < len(right):
        return 1
    return 0


def parse(elem: str) -> Value:
    return eval(elem)


def task1(text: str) -> int:
    pairs = text.strip().split("\n\n")
    s = 0
    for i, pair in enumerate(pairs):
        left, right = (parse(e) for e in pair.split("\n"))
        if cmp(left, right) == 1:
            s += i+1
    return s


def task2(text: str) -> int:
    lines = text.strip().split()
    packets = [parse(e) for e in lines]
    divider1 = [[2]]
    divider2 = [[6]]
    divider1pos = [cmp(packet, divider1) for packet in packets].count(1) + 1
    divider2pos = [cmp(packet, divider2) for packet in packets].count(1) + 2

    return divider1pos * divider2pos


inp = fts("13in.txt")
print(task1(inp))
print(task2(inp))
