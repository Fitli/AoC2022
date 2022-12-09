from typing import List


def file_to_grid(filename):
    with open(filename) as f:
        lines = list(map(lambda x: list(x.strip()), f.readlines()))
    for i in range(len(lines)):
        lines[i] = list(map(int, lines[i]))
    return lines


def is_visible_line(tree_line: List[int]) -> List[bool]:
    highest = -1
    visible = []
    for tree in tree_line:
        if tree > highest:
            visible.append(True)
            highest = tree
        else:
            visible.append(False)
    return visible


def task1(trees: List[List[int]]):
    width, height = len(trees[0]), len(trees)
    is_visible = [[False] * width for _ in range(height)]
    for i in range(height):
        left_to_right = is_visible_line(trees[i])
        right_to_left = is_visible_line(trees[i][::-1])[::-1]
        is_visible[i] = [x or y or z for (x, y, z) in zip(is_visible[i], left_to_right,
                                                          right_to_left)]
    for j in range(width):
        col = [trees[i][j] for i in range(height)]
        top_to_bottom = is_visible_line(col)
        bottom_to_top = is_visible_line(col[::-1])[::-1]
        for i in range(height):
            is_visible[i][j] = is_visible[i][j] or top_to_bottom[i] or bottom_to_top[i]
    return sum(map(lambda x: x.count(True), is_visible))


def scenic_line(tree_line: List[int]) -> List[int]:
    high_trees: List[int] = []
    scores: List[int] = []
    for i in range(len(tree_line)):
        visible = 0
        for k in range(len(high_trees) - 1, -1, -1):
            if tree_line[i] > tree_line[high_trees[k]]:
                high_trees.pop()
            else:
                visible = i - high_trees[k]
                high_trees.append(i)
                break
        if not high_trees:
            visible = i
            high_trees.append(i)
        scores.append(visible)
    return scores


def task2(trees: List[List[int]]):
    width, height = len(trees[0]), len(trees)
    scenic_score = [[1] * width for _ in range(height)]
    for i in range(height):
        left_to_right = scenic_line(trees[i])
        right_to_left = scenic_line(trees[i][::-1])[::-1]
        scenic_score[i] = [x * y * z for (x, y, z) in zip(scenic_score[i], left_to_right,
                                                          right_to_left)]
    for j in range(width):
        col = [trees[i][j] for i in range(height)]
        top_to_bottom = scenic_line(col)
        bottom_to_top = scenic_line(col[::-1])[::-1]
        for i in range(height):
            scenic_score[i][j] = scenic_score[i][j] * top_to_bottom[i] * bottom_to_top[i]
    return max(map(max, scenic_score))


grid = file_to_grid("08in.txt")
print(task1(grid))
print(task2(grid))
