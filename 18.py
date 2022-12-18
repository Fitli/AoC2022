def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def neighbours(block):
    x,y,z = block
    neighbours = []
    for d in (1, -1):
        neighbours.append((x+d,y,z))
        neighbours.append((x,y+d,z))
        neighbours.append((x,y,z+d))
    return neighbours

def outside(blocks):
    minx, maxx = min([x for x,_,_ in blocks]) - 1, max([x for x,_,_ in blocks]) + 1
    miny, maxy = min([y for _,y,_ in blocks]) - 1, max([y for _,y,_ in blocks]) + 1
    minz, maxz = min([z for _,_,z in blocks]) - 1, max([z for _,_,z in blocks]) + 1
    outside = {(minx, miny, minz)}
    to_inspect = {(minx, miny, minz)}
    while(to_inspect):
        block = to_inspect.pop()
        neighs = {n for n in neighbours(block) if minx <= n[0] <= maxx
                  and miny <= n[1] <= maxy and minz <= n[2] <= maxz
                  and n not in outside and n not in blocks}
        outside.update(neighs)
        to_inspect.update(neighs)
    return outside


def task1(text):
    count = 0
    blocks = set()
    for line in text.strip().split("\n"):
        blocks.add(tuple(map(int,line.split(","))))
    for block in blocks:
        for neigh in neighbours(block):
            if neigh not in blocks:
                count += 1
    return count




def task2(text):
    count = 0
    blocks = set()
    for line in text.strip().split("\n"):
        blocks.add(tuple(map(int, line.split(","))))
    outs = outside(blocks)
    for block in blocks:
        for neigh in neighbours(block):
            if neigh in outs:
                count += 1
    return count


if __name__ == "__main__":
    inp = fts("18in.txt")
    print(task1(inp))
    print(task2(inp))
