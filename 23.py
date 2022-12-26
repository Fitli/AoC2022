import time


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def parse(text):
    elves = []
    lines = text.strip().split("\n")
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == "#":
                elves.append((j, i))
    return elves

def neigh(elf):
    x, y = elf
    n = {(x_, y_) for x_ in [x+1, x, x-1] for y_ in [y+1, y, y-1]}
    n.remove(elf)
    return n

def neighN(elf):
    x, y = elf
    return {(x_, y-1) for x_ in [x-1, x, x+1]}

def neighS(elf):
    x, y = elf
    return {(x_, y+1) for x_ in [x-1, x, x+1]}

def neighW(elf):
    x, y = elf
    return {(x-1, y_) for y_ in [y-1, y, y+1]}

def neighE(elf):
    x, y = elf
    return {(x+1, y_) for y_ in [y-1, y, y+1]}

DIRECTIONS = [
    (neighN, (0, -1)),
    (neighS, (0, 1)),
    (neighW, (-1, 0)),
    (neighE, (1, 0))
]

def simulate_step(elves, iter):
    change = False
    positions = set(elves)
    considered_moves = []
    pos1 = set()
    pos2 = set()
    for elf in elves:
        move = None
        if not positions.intersection(neigh(elf)):
            pass
        else:
            for i in range(len(DIRECTIONS)):
                d = (iter+i)%len(DIRECTIONS)
                if not DIRECTIONS[d][0](elf).intersection(positions):
                    move = (elf[0] + DIRECTIONS[d][1][0], elf[1] + DIRECTIONS[d][1][1])
                    break
        considered_moves.append(move)
        if move in pos1:
            pos2.add(move)
        pos1.add(move)
    for i in range(len(elves)):
        if considered_moves[i] and considered_moves[i] not in pos2:
            elves[i] = considered_moves[i]
            change = True
    return change

def count_empty(elves):
    minx = min([elf[0] for elf in elves])
    maxx = max([elf[0] for elf in elves])
    miny = min([elf[1] for elf in elves])
    maxy = max([elf[1] for elf in elves])
    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves)

def print_elves(elves):
    for i in range(-2, 10):
        for j in range(-3, 11):
            if (j, i) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


def task1(text):
    elves = parse(text)
    for i in range(10):
        simulate_step(elves, i)
    return count_empty(elves)


def task2(text: str):
    elves = parse(text)
    i = 0
    while simulate_step(elves, i):
        i += 1
    return i + 1


if __name__ == "__main__":
    start_t = time.time()
    inp = fts("23in.txt")
    print(task1(inp))
    print(f"{time.time() - start_t} s")
    start_t = time.time()
    print(task2(inp))
    print(f"{time.time() - start_t} s")
