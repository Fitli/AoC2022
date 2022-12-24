import time
from typing import Tuple, List, Set, Collection


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Blizzard:
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = direction

    def move(self):
        if self.dir == ">":
            self.x = (self.x+1) % self.width
        elif self.dir == "<":
            self.x = (self.x - 1) % self.width
        elif self.dir == "v":
            self.y = (self.y+1) % self.height
        elif self.dir == "^":
            self.y = (self.y - 1) % self.height


class Map:
    def __init__(self, walls, width, height, start: Tuple[int, int], end: Tuple[int, int]):
        self.walls = walls
        self.width = width
        self.height = height
        self.start = start
        self.end = end


def parse(text: str) -> Tuple[List[Blizzard], Map]:
    lines = text.strip().split()
    height = len(lines)
    width = len(lines[0])
    walls = set()
    blizzards = []
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == "#":
                walls.add((j, i))
            elif ch != ".":
                blizzards.append(Blizzard(j-1, i-1, width - 2, height - 2, ch))

    return blizzards, Map(walls, width, height, (1, 0), (width - 2, height - 1))


def neighbors(position: Tuple[int, int], blizzards: Collection[Blizzard], mapa: Map) \
        -> Set[Tuple[int, int]]:
    blizzard_positions = {(b.x+1, b.y+1) for b in blizzards}
    neighs = set()
    x, y = position
    if (x,y) not in blizzard_positions:
        neighs.add((x,y))
    if x > 0 and (x - 1, y) not in mapa.walls and (x - 1, y) not in blizzard_positions:
        neighs.add((x - 1, y))
    if y > 0 and (x, y - 1) not in mapa.walls and (x, y - 1) not in blizzard_positions:
        neighs.add((x, y - 1))
    if x < mapa.width - 1 and (x + 1, y) not in mapa.walls and (x + 1, y) not in blizzard_positions:
        neighs.add((x + 1, y))
    if y < mapa.height - 1 and (x, y + 1) not in mapa.walls and (
    x, y + 1) not in blizzard_positions:
        neighs.add((x, y + 1))
    return neighs

def go_from_to(mapa, blizzards, start, end):
    possible_positions = {start}
    counter = 0
    while end not in possible_positions:
        for blizz in blizzards:
            blizz.move()
        new_positions = set()
        for pos in possible_positions:
            new_positions.update(neighbors(pos, blizzards, mapa))
        possible_positions = new_positions
        counter += 1
    return counter

def task1(text: str):
    blizzards, mapa = parse(text)
    counter = 0
    counter += go_from_to(mapa, blizzards, mapa.start, mapa.end)
    return counter

def task2(text: str):
    blizzards, mapa = parse(text)
    counter = 0
    counter += go_from_to(mapa, blizzards, mapa.start, mapa.end)
    counter += go_from_to(mapa, blizzards, mapa.end, mapa.start)
    counter += go_from_to(mapa, blizzards, mapa.start, mapa.end)
    return counter


if __name__ == "__main__":
    start_t = time.time()
    inp = fts("24in.txt")
    print(task1(inp))
    print(f"{time.time() - start_t} s")
    start_t = time.time()
    print(task2(inp))
    print(f"{time.time() - start_t} s")
