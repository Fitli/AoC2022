from typing import Tuple, Set

Coordinates = Tuple[int, int]


def load_map(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    mapa = list(map(list, lines))
    return mapa


def neighbours(coords, height, width):
    y, x = coords
    neighs = set()
    if x > 0:
        neighs.add((y, x - 1))
    if x < width - 1:
        neighs.add((y, x + 1))
    if y > 0:
        neighs.add((y - 1, x))
    if y < height - 1:
        neighs.add((y + 1, x))
    return neighs


def task1(mapa):
    reachable: Set[Coordinates] = set()
    visited: Set[Coordinates] = set()
    height, width = len(mapa), len(mapa[0])
    for i in range(height):
        for j in range(width):
            if mapa[i][j] == "S":
                reachable.add((i, j))
                mapa[i][j] = "a"
            if mapa[i][j] == "E":
                destination = (i, j)
                mapa[i][j] = "z"
            mapa[i][j] = ord(mapa[i][j]) - ord("a")
    it = 0
    while destination not in reachable:
        visited.update(reachable)
        new_reachable = set()
        for (i, j) in reachable:
            for (ni, nj) in neighbours((i, j), height, width):
                if mapa[ni][nj] <= mapa[i][j] + 1 and (ni, nj) not in visited:
                    new_reachable.add((ni, nj))
        reachable = new_reachable
        it += 1
    return it


def task2(mapa):
    reachable = set()
    visited = set()
    height, width = len(mapa), len(mapa[0])
    destinations = set()
    for i in range(height):
        for j in range(width):
            if mapa[i][j] == "E":
                reachable.add((i, j))
                mapa[i][j] = "z"
            if mapa[i][j] == "S":
                mapa[i][j] = "a"
            if mapa[i][j] == "a":
                destinations.add((i, j))
            mapa[i][j] = ord(mapa[i][j]) - ord("a")
    it = 0
    visited.update(reachable)
    while not destinations.intersection(visited):
        new_reachable = set()
        for (i, j) in reachable:
            for (ni, nj) in neighbours((i, j), height, width):
                if mapa[ni][nj] >= mapa[i][j] - 1 and (ni, nj) not in visited:
                    new_reachable.add((ni, nj))
        reachable = new_reachable
        it += 1
        visited.update(reachable)
    return it


inp = load_map("12in.txt")
print(task1(inp))
inp = load_map("12in.txt")
print(task2(inp))
