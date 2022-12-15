from collections import namedtuple
from typing import Set, List

Coordinates = namedtuple("Coordinates", "x y")
Column = List[bool]
Plan = List[Column]


class Cave:
    def __init__(self, lines):
        block_set = set()
        for line in lines:
            corners = line.split(" -> ")
            x, y = map(int, corners[0].split(","))
            start = Coordinates(x, y)
            for i in range(1, len(corners)):
                x, y = map(int, corners[i].split(","))
                end = Coordinates(x, y)
                bulid_line(start, end, block_set)
                start = end
        maxy = max({block.y for block in block_set})
        maxx = 500 + maxy + 5
        minx = 500 - maxy - 5
        self.rocks = []
        for c in range(maxx - minx + 1):
            self.rocks.append([False] * (maxy + 1))
        for block in block_set:
            self.rocks[block.x - minx][block.y] = True
        self.hole = 500 - minx
        self.floor = False

    def add_floor(self):
        for col in self.rocks:
            col.append(False)
            col.append(True)
        self.floor = True

    def pour(self):
        x = self.hole
        y = 0
        if self.rocks[x][y]:
            return False
        while True:
            if y == len(self.rocks[x]) - 1:
                return False
            if not self.rocks[x][y + 1]:
                y += 1
                continue
            elif not self.rocks[x - 1][y + 1]:
                x -= 1
                y += 1
                continue
            elif not self.rocks[x + 1][y + 1]:
                x += 1
                y += 1
                continue
            self.rocks[x][y] = True
            return True

    def count2(self):
        sand = []
        for col in self.rocks:
            sand.append([False] * len(col))
        sand[self.hole][0] = True
        count = 1
        for row in range(1, len(sand[0])):
            for col in range(1, len(sand) - 1):
                if not self.rocks[col][row] and (sand[col][row - 1] or
                                                 sand[col-1][row-1] or sand[col+1][row-1]):
                    sand[col][row] = True
                    count += 1
        return count


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def bulid_line(start: Coordinates, end: Coordinates, block_set: Set[Coordinates]):
    if start.x < end.x:
        dx = 1
    if start.x == end.x:
        dx = 0
    if start.x > end.x:
        dx = -1
    if start.y < end.y:
        dy = 1
    if start.y == end.y:
        dy = 0
    if start.y > end.y:
        dy = -1

    x, y = start.x, start.y
    while x != end.x or y != end.y:
        block_set.add(Coordinates(x, y))
        x += dx
        y += dy
    block_set.add(end)


def task1(text):
    lines = text.strip().split("\n")
    cave = Cave(lines)
    count = 0
    while cave.pour():
        count += 1
    return count


def task2(text):
    lines = text.strip().split("\n")
    cave = Cave(lines)
    cave.add_floor()
    return cave.count2()


if __name__ == "__main__":
    inp = fts("14in.txt")
    print(task1(inp))
    print(task2(inp))
