from typing import List, Optional
import time


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Tile:
    def __init__(self, exists, is_wall, x, y):
        self.exists = exists
        self.wall = is_wall

        self.x = x
        self.y = y
        self.nighbours = [None, None, None, None]


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
    def __init__(self, mapa: List[List[Optional[Tile]]]):
        self.mapa = mapa
        self.x = min([x for x in range(len(mapa[0])) if mapa[0][x].exists])
        self.y = 0
        self.field = mapa[self.y][self.x]
        self.facing = 0

    def perform(self, instr: Instruction):
        self.facing += instr.dir
        self.facing %= 4
        for _ in range(instr.dist):
            if self.field.nighbours[self.facing]:
                new_field = self.field.nighbours[self.facing]
                self.field = new_field
            else:
                break

    def calculate_password(self):
        return 1000 * (self.field.y + 1) + 4 * (self.field.x + 1) + self.facing

def assign_neighbors(mapa: List[List[Optional[Tile]]]):
    col_starts = []
    col_ends = []
    for c in range(len(mapa[0])):
        c_exist = [i for i in range(len(mapa)) if mapa[i][c].exists]
        col_starts.append(min(c_exist))
        col_ends.append(max(c_exist))
    for l in range(len(mapa)):
        line_start = min([i for i in range(len(mapa[l])) if mapa[l][i].exists])
        line_end = max([i for i in range(len(mapa[l])) if mapa[l][i].exists])
        for c in range(len(mapa[l])):
            if not mapa[l][c].exists:
                continue
            if c == line_end:
                mapa[l][c].nighbours[0] = mapa[l][line_start]
            else:
                mapa[l][c].nighbours[0] = mapa[l][c+1]
            if l == col_ends[c]:
                mapa[l][c].nighbours[1] = mapa[col_starts[c]][c]
            else:
                mapa[l][c].nighbours[1] = mapa[l+1][c]
            if c == line_start:
                mapa[l][c].nighbours[2] = mapa[l][line_end]
            else:
                mapa[l][c].nighbours[2] = mapa[l][c-1]
            if l == col_starts[c]:
                mapa[l][c].nighbours[3] = mapa[col_ends[c]][c]
            else:
                mapa[l][c].nighbours[3] = mapa[l-1][c]
            for dir in range(4):
                if mapa[l][c].nighbours[dir].wall:
                    mapa[l][c].nighbours[dir] = None


def parse(text:str):
    lines = text.rstrip().split("\n")
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
                mapa[i].append(Tile(True, False, j, i))
            if ch == "#":
                mapa[i].append(Tile(True, True, j, i))
        for j in range(len(line), width):
            mapa[i].append(Tile(False, False, j, i))

    assign_neighbors(mapa)

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


def task1(text:str):
    mapa, instructions = parse(text)

    walker = Walker(mapa)
    for instruction in instructions:
        #print(instruction.dist, instruction.dir)
        walker.perform(instruction)
        #print(walker.field.x, walker.field.y, walker.facing)

    return walker.calculate_password()


def task2(text):
    return "TODO"


if __name__ == "__main__":
    start = time.time()
    inp = fts("22in.txt")
    #inp = fts("22small.txt")
    print(task1(inp))
    print(f"{time.time() - start} s")
    start = time.time()
    print(task2(inp))
    print(f"{time.time() - start} s")
