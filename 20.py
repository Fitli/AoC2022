from collections import deque


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def mix(numbers, iters):
    nums = [(n%(len(numbers) - 1), i) for i, n in enumerate(numbers)]
    dq = deque(nums)
    for _ in range(iters):
        for elem in nums:
            pos = dq.index(elem)
            dq.rotate(-pos)
            moved = dq.popleft()
            step = moved[0]
            dq.rotate(-step)
            dq.appendleft(moved)
            dq.rotate(step)
            dq.rotate(pos)
    return [numbers[i] for _, i in dq]


def get_score(numbers):
    zero = 0
    for i, n in enumerate(numbers):
        if n == 0:
            zero = i
    return sum([numbers[(zero + i*1000) % len(numbers)] for i in range(1, 4)])


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
