def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def neighbours(block):
    x, y, z = block
    neighs = []
    for d in (1, -1):
        neighs.append((x + d, y, z))
        neighs.append((x, y + d, z))
        neighs.append((x, y, z + d))
    return neighs


def outside(blocks):
    mins = tuple(min(block[i]-1 for block in blocks) for i in range(3))
    maxs = tuple(max(block[i]+1 for block in blocks) for i in range(3))
    outs = {mins, maxs}
    to_inspect = {mins, maxs}
    while to_inspect:
        block = to_inspect.pop()
        neighs = {n for n in neighbours(block) if
                  all([mins[i] <= n[i] <= maxs[i] for i in range(3)])
                  and n not in outs and n not in blocks}
        outs.update(neighs)
        to_inspect.update(neighs)
    return outs


def task1(text):
    blocks = {tuple(map(int, line.split(","))) for line in text.strip().split("\n")}
    return sum([(n not in blocks) for block in blocks for n in neighbours(block)])


def task2(text):
    blocks = {tuple(map(int, line.split(","))) for line in text.strip().split("\n")}
    outs = outside(blocks)
    return sum([(n in outs) for block in blocks for n in neighbours(block)])


if __name__ == "__main__":
    inp = fts("18in.txt")
    print(task1(inp))
    print(task2(inp))
