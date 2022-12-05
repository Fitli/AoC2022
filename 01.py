from typing import List


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def task1(inp: str) -> int:
    elfs = inp.split("\n\n")
    cals = [sum(map(int, elf.split())) for elf in elfs]
    return max(cals)


# I just admit to sort the whole thing because of 3 elements...
def check(suma: int, max3: List[int]):
    for i in range(1, 4):
        if suma >= max3[-i]:
            max3.insert(3 - i + 1, suma)
            max3.pop(0)
            break


def task2(inp: str) -> int:
    elfs = inp.split("\n\n")
    cals = [sum(map(int, elf.split())) for elf in elfs]
    max3 = [0, 0, 0]
    for elf in cals:
        check(elf, max3)
    return sum(max3)


text = fts("01in.txt")
print(task1(text))
print(task2(text))
