from typing import List


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class ListElem:
    def __init__(self, val, pos):
        self.val = val
        self.orig_pos = pos


def move(lst: List[ListElem], pos, positions: List[int]):
    el = lst[pos]
    dest_pos = (pos + el.val % (len(lst) - 1)) % (len(lst) - 1)
    if dest_pos == 0:
        dest_pos = len(lst)
    if dest_pos > pos:
        beg = lst[:pos]
        mid = lst[pos + 1:dest_pos + 1]
        end = lst[dest_pos + 1:]
        lst = beg + mid + [el] + end
    else:
        beg = lst[:dest_pos]
        mid = lst[dest_pos:pos]
        end = lst[pos + 1:]
        lst = beg + [el] + mid + end
    for i, el in enumerate(lst):
        positions[el.orig_pos] = i
    return lst


def mix(numbers, iters):
    positions = []
    elems: List[ListElem] = []
    for i, n in enumerate(numbers):
        positions.append(i)
        elems.append(ListElem(n, i))
    for _ in range(iters):
        for p in positions:
            elems = move(elems, p, positions)
    return [e.val for e in elems]


def get_score(numbers):
    zero = 0
    for i, n in enumerate(numbers):
        if n == 0:
            zero = i
    return numbers[(zero + 1000) % len(numbers)] + \
           numbers[(zero + 2000) % len(numbers)] + \
           numbers[(zero + 3000) % len(numbers)]


def task1(text):
    numbers = list(map(int, text.strip().split()))
    numbers = mix(numbers, 1)
    return get_score(numbers)


def task2(text):
    numbers = list(map(lambda x: int(x) * 811589153, text.strip().split()))
    numbers = mix(numbers, 10)
    return get_score(numbers)


if __name__ == "__main__":
    inp = fts("20in.txt")
    print(task1(inp))
    print(task2(inp))
