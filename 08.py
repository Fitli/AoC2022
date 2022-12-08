from typing import List, Tuple


def file_to_grid(filename):
    with open(filename) as f:
        lines = list(map(lambda x: list(x.strip()), f.readlines()))
    for i in range(len(lines)):
        lines[i] = list(map(int, lines[i]))
    return lines


def task1(trees: List[List[int]]):
    width, height = len(trees[0]), len(trees)
    is_visible = [[False] * width for _ in range(height)]
    for i in range(height):
        highest = -1
        for j in range(width):
            if trees[i][j] > highest:
                is_visible[i][j] = True
                highest = trees[i][j]
        highest = -1
        for j in range(width - 1, -1, -1):
            if trees[i][j] > highest:
                is_visible[i][j] = True
                highest = trees[i][j]
    for j in range(width):
        highest = -1
        for i in range(height):
            if trees[i][j] > highest:
                is_visible[i][j] = True
                highest = trees[i][j]
        highest = -1
        for i in range(height - 1, -1, -1):
            if trees[i][j] > highest:
                is_visible[i][j] = True
                highest = trees[i][j]
    return sum(map(lambda x: x.count(True), is_visible))


def task2(trees: List[List[int]]):
    width, height = len(trees[0]), len(trees)
    scenic_score = [[1] * width for _ in range(height)]
    for i in range(height):
        high_trees: List[Tuple[int, int]] = []
        for j in range(width):
            visible = 0
            for k in range(len(high_trees) - 1, -1, -1):
                if trees[i][j] > trees[high_trees[k][0]][high_trees[k][1]]:
                    high_trees.pop()
                else:
                    visible = j - high_trees[k][1]
                    high_trees.append((i, j))
                    break
            if not high_trees:
                visible = j
                high_trees.append((i, j))
            scenic_score[i][j] *= visible
        high_trees: List[Tuple[int, int]] = []
        for j in range(width - 1, -1, -1):
            visible = 0
            for k in range(len(high_trees) - 1, -1, -1):
                if trees[i][j] > trees[high_trees[k][0]][high_trees[k][1]]:
                    high_trees.pop()
                else:
                    visible = high_trees[k][1] - j
                    high_trees.append((i, j))
                    break
            if not high_trees:
                visible = width - 1 - j
                high_trees.append((i, j))
            scenic_score[i][j] *= visible
    for j in range(width):
        high_trees: List[Tuple[int, int]] = []
        for i in range(height):
            visible = 0
            for k in range(len(high_trees) - 1, -1, -1):
                if trees[i][j] > trees[high_trees[k][0]][high_trees[k][1]]:
                    high_trees.pop()
                else:
                    visible = i - high_trees[k][0]
                    high_trees.append((i, j))
                    break
            if not high_trees:
                visible = i
                high_trees.append((i, j))
            scenic_score[i][j] *= visible
        high_trees: List[Tuple[int, int]] = []
        for i in range(height - 1, -1, -1):
            visible = 0
            for k in range(len(high_trees) - 1, -1, -1):
                if trees[i][j] > trees[high_trees[k][0]][high_trees[k][1]]:
                    high_trees.pop()
                else:
                    visible = high_trees[k][0] - i
                    high_trees.append((i, j))
                    break
            if not high_trees:
                visible = height - 1 - i
                high_trees.append((i, j))
            scenic_score[i][j] *= visible
    return max(map(max, scenic_score))


grid = file_to_grid("08in.txt")
print(task1(grid))
print(task2(grid))
