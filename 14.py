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
        maxx = max({block.x for block in block_set})
        minx = min({block.x for block in block_set})
        self.plan = []
        for c in range(maxx - minx + 1):
            self.plan.append([False] * (maxy + 1))
        for block in block_set:
            self.plan[block.x - minx][block.y] = True
        self.hole = 500 - minx
        self.floor = False

    def add_floor(self):
        for col in self.plan:
            col.append(False)
            col.append(True)
        self.floor = True

    def add_col_left(self):
        self.plan.insert(0, [False] * len(self.plan[0]))
        if self.floor:
            self.plan[0][-1] = True

    def add_col_right(self):
        self.plan.append([False] * len(self.plan[0]))
        if self.floor:
            self.plan[-1][-1] = True

    def pour(self):
        x = self.hole
        y = 0
        if self.plan[x][y]:
            return False
        while True:
            if x == 0:
                self.add_col_left()
                x += 1
                self.hole += 1
            if x == len(self.plan) - 1:
                self.add_col_right()
            if y == len(self.plan[x]) - 1:
                return False
            if not self.plan[x][y + 1]:
                y += 1
                continue
            elif not self.plan[x - 1][y + 1]:
                x -= 1
                y += 1
                continue
            elif not self.plan[x + 1][y + 1]:
                x += 1
                y += 1
                continue
            self.plan[x][y] = True
            return True


def ftl(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


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


def task1(lines):
    cave = Cave(lines)
    count = 0
    while cave.pour():
        count += 1
    return count


def task2(lines):
    cave = Cave(lines)
    cave.add_floor()
    count = 0
    while cave.pour():
        count += 1
    return count


inp = ftl("14in.txt")
print(task1(inp))
print(task2(inp))
