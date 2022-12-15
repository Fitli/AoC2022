def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def to_priority(item: str) -> int:
    if item == item.lower():
        return ord(item)-ord("a")+1
    else:
        return ord(item)-ord("A")+27


def task1(text: str) -> int:
    lines = text.split()
    suma = 0
    for line in lines:
        middle = len(line)//2
        letters = set(line[:middle])
        for i in range(middle, middle*2):
            if line[i] in letters:
                suma += to_priority(line[i])
                break
    return suma


def task2(text: str) -> int:
    lines = text.split()
    suma = 0
    for i in range(0, len(lines), 3):
        letters = set(lines[i])\
            .intersection(lines[i+1])\
            .intersection(lines[i+2])
        suma += to_priority(letters.pop())
    return suma


if __name__ == "__main__":
    inp = fts("03in.txt")
    print(task1(inp))
    print(task2(inp))
