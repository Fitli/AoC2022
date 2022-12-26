import time
from typing import Tuple, Set


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Map:
    def __init__(self, width, height, start: Tuple[int, int], end: Tuple[int, int],
                 blizzards: Set[Tuple[int, int, str]]):
        self.blizards = blizzards
        self.width = width
        self.height = height
        self.start = start
        self.end = end


def parse(text: str) -> Map:
    lines = text.strip().split()
    height = len(lines)
    width = len(lines[0])
    blizzards = set()
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch != ".":
                blizzards.add((j, i, ch))

    return Map(width, height, (1, 0), (width - 2, height - 1), blizzards)


def comming_blizzard(mapa: Map, pos, minutes):
    x, y = pos
    if (x, y, "#") in mapa.blizards:
        return True
    if ((x - 1 + minutes) % (mapa.width - 2) + 1, y, "<") in mapa.blizards:
        return True
    if ((x - 1 - minutes) % (mapa.width - 2) + 1, y, ">") in mapa.blizards:
        return True
    if (x, (y - 1 + minutes) % (mapa.height - 2) + 1, "^") in mapa.blizards:
        return True
    if (x, (y - 1 - minutes) % (mapa.height - 2) + 1, "v") in mapa.blizards:
        return True
    return False


def neighbors(position: Tuple[int, int], mapa: Map, minutes: int) \
        -> Set[Tuple[int, int]]:
    neighs = set()
    x, y = position
    if not comming_blizzard(mapa, (x, y), minutes):
        neighs.add((x, y))
    if x > 0 and not comming_blizzard(mapa, (x - 1, y), minutes):
        neighs.add((x - 1, y))
    if y > 0 and not comming_blizzard(mapa, (x, y - 1), minutes):
        neighs.add((x, y - 1))
    if x < mapa.width - 1 and not comming_blizzard(mapa, (x + 1, y), minutes):
        neighs.add((x + 1, y))
    if y < mapa.height - 1 and not comming_blizzard(mapa, (x, y + 1), minutes):
        neighs.add((x, y + 1))
    return neighs


def go_from_to(mapa, start, end, init_t):
    possible_positions = {start}
    counter = 0
    while end not in possible_positions:
        counter += 1
        new_positions = set()
        for pos in possible_positions:
            new_positions.update(neighbors(pos, mapa, init_t + counter))
        possible_positions = new_positions
    return counter


def task1(text: str):
    mapa = parse(text)
    counter = 0
    counter += go_from_to(mapa, mapa.start, mapa.end, 0)
    return counter


def task2(text: str):
    mapa = parse(text)
    counter = 0
    counter += go_from_to(mapa, mapa.start, mapa.end, 0)
    counter += go_from_to(mapa, mapa.end, mapa.start, counter)
    counter += go_from_to(mapa, mapa.start, mapa.end, counter)
    return counter


if __name__ == "__main__":
    start_t = time.time()
    inp = fts("24in.txt")
    print(task1(inp))
    print(f"{time.time() - start_t} s")
    start_t = time.time()
    print(task2(inp))
    print(f"{time.time() - start_t} s")
