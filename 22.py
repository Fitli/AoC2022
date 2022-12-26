from math import sqrt
from typing import List, Optional, Set
import time


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Tile:
    def __init__(self, exists, is_wall, x, y):
        self.exists = exists
        self.wall = is_wall

        self.x = x
        self.y = y
        self.neighbors: List[Optional['Tile']] = [None, None, None, None]
        self.new_directs: List[int] = [0, 0, 0, 0]

    def glue(self, other: 'Tile', direc: int, other_dir: int):
        self.neighbors[direc] = other
        self.new_directs[direc] = (other_dir + 2) % 4
        other.neighbors[other_dir] = self
        other.new_directs[other_dir] = (direc + 2) % 4


Mapa = List[List[Optional[Tile]]]


class Instruction:
    def __init__(self, instr: str):
        if instr == "L":
            self.dir = -1
            self.dist = 0
        elif instr == "R":
            self.dir = 1
            self.dist = 0
        else:
            self.dir = 0
            self.dist = int(instr)


class Walker:
    def __init__(self, mapa: Mapa):
        self.mapa = mapa
        self.x = min([x for x in range(len(mapa[0])) if mapa[0][x].exists])
        self.y = 0
        self.field = mapa[self.y][self.x]
        self.facing = 0

    def perform(self, instr: Instruction):
        self.facing += instr.dir
        self.facing %= 4
        for _ in range(instr.dist):
            if not self.field.neighbors[self.facing].wall:
                new_field = self.field.neighbors[self.facing]
                new_dir = self.field.new_directs[self.facing]
                self.field = new_field
                self.facing = new_dir
            else:
                break
        self.x = self.field.x
        self.y = self.field.y

    def calculate_password(self):
        return 1000 * (self.field.y + 1) + 4 * (self.field.x + 1) + self.facing


def assign_neighbors(mapa: Mapa):
    for l in range(len(mapa)):
        for c in range(len(mapa[l])):
            if not mapa[l][c].exists:
                continue
            for d in range(len(directions)):
                dl, dc = directions[d]
                if 0 <= l + dl < len(mapa) and 0 <= c + dc < len(mapa[l]):
                    n = mapa[l + dl][c + dc]
                    if n.exists:
                        mapa[l][c].neighbors[d] = n
                        mapa[l][c].new_directs[d] = d
                else:
                    mapa[l][c].neighbors[d] = None


def glue1(mapa: Mapa):
    for l in range(len(mapa)):
        line_start = min([i for i in range(len(mapa[l])) if mapa[l][i].exists])
        line_end = max([i for i in range(len(mapa[l])) if mapa[l][i].exists])
        mapa[l][line_end].glue(mapa[l][line_start], 0, 2)
    for c in range(len(mapa[0])):
        col_start = min([i for i in range(len(mapa)) if mapa[i][c].exists])
        col_end = max([i for i in range(len(mapa)) if mapa[i][c].exists])
        mapa[col_end][c].glue(mapa[col_start][c], 1, 3)


def find_friend(field):
    miss_d = [d for d in range(len(directions)) if not field.neighbors[d]][0]
    for i in range(4):
        f1 = field.neighbors[i]
        if not f1:
            continue
        nn = len([d for d in range(len(directions)) if f1.neighbors[d]])
        if nn != 4:
            continue
        for j in range(4):
            f2 = field.neighbors[i].neighbors[j]
            if not f2 or f2 == field:
                continue
            nn = len([d for d in range(len(directions)) if f2.neighbors[d]])
            if nn == 3:
                miss_d2 = [d for d in range(len(directions)) if not f2.neighbors[d]][0]
                return f2, miss_d, (i + 2) % 4, miss_d2, f1.new_directs[j]
    return None, 0, 0, 0, 0


def glue2(mapa: Mapa, square_size):
    corners: Set[Tile] = set()
    height = len(mapa)
    width = len(mapa[0])
    for l in list(range(0, height, square_size)) + list(
            range(square_size - 1, height, square_size)):
        for c in list(range(0, width, square_size)) + list(
                range(square_size - 1, width, square_size)):
            corners.add(mapa[l][c])
    while True:
        other = None
        for corner in list(corners):
            nn = len([d for d in range(len(directions)) if corner.neighbors[d]])
            if nn == 4 or nn == 0:
                corners.remove(corner)
            if nn == 3:
                other, gd1, d1, gd2, d2 = find_friend(corner)
                if other:
                    c = corner
                    break
        if not other:
            break
        for i in range(square_size):
            c.glue(other, gd1, gd2)
            c = c.neighbors[d1]
            other = other.neighbors[d2]


def parse(text: str, task: int):
    lines = text.rstrip().split("\n")
    num_fields = 0
    map_lines = lines[:-2]
    instruction_line = lines[-1]
    mapa: List[List[Optional[Tile]]] = []
    width = max([len(l) for l in map_lines])
    for i, line in enumerate(map_lines):
        mapa.append([])
        for j, ch in enumerate(line):
            if ch == " ":
                mapa[i].append(Tile(False, False, j, i))
            if ch == ".":
                num_fields += 1
                mapa[i].append(Tile(True, False, j, i))
            if ch == "#":
                num_fields += 1
                mapa[i].append(Tile(True, True, j, i))
        for j in range(len(line), width):
            mapa[i].append(Tile(False, False, j, i))

    square_size = int(sqrt(num_fields // 6))
    assign_neighbors(mapa)
    if task == 1:
        glue1(mapa)
    else:
        glue2(mapa, square_size)

    instructions = []
    curr = ""
    for ch in instruction_line:
        if ch in {"L", "R"}:
            if curr:
                instructions.append(Instruction(curr))
            instructions.append(Instruction(ch))
            curr = ""
        else:
            curr += ch
    if curr:
        instructions.append(Instruction(curr))
    return mapa, instructions


def task1(text: str):
    mapa, instructions = parse(text, 1)
    walker = Walker(mapa)
    for instruction in instructions:
        walker.perform(instruction)
    return walker.calculate_password()


def task2(text: str):
    mapa, instructions = parse(text, 2)
    walker = Walker(mapa)
    for instruction in instructions:
        walker.perform(instruction)
    return walker.calculate_password()


if __name__ == "__main__":
    start = time.time()
    inp = fts("22in.txt")
    # inp = fts("22small.txt")
    print(task1(inp))
    print(f"{time.time() - start} s")
    start = time.time()
    print(task2(inp))
    print(f"{time.time() - start} s")
