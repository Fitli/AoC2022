from collections import namedtuple
Coordinates = namedtuple("Coordinates", "x y")


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def move_head(head: Coordinates, direction: str) -> Coordinates:
    if direction == "R":
        return Coordinates(head.x+1, head.y)
    if direction == "L":
        return Coordinates(head.x-1, head.y)
    if direction == "U":
        return Coordinates(head.x, head.y+1)
    if direction == "D":
        return Coordinates(head.x, head.y-1)


def move_tail(tail: Coordinates, head: Coordinates) -> Coordinates:
    dx = head.x - tail.x
    dy = head.y - tail.y
    if abs(dx) == 2 and abs(dy) == 2:
        return Coordinates(tail.x + dx // 2, tail.y + dy // 2)
    elif abs(dx) == 2:
        return Coordinates(tail.x + dx//2, head.y)
    elif abs(dy) == 2:
        return Coordinates(head.x, tail.y + dy//2)
    return tail


def simulate(lines, num_knots):
    knots = [Coordinates(0, 0)] * num_knots
    tail_set = {knots[-1]}
    for line in lines:
        direction, distance = line.split()
        distance = int(distance)
        for _ in range(distance):
            knots[0] = move_head(knots[0], direction)
            for i in range(1, num_knots):
                knots[i] = move_tail(knots[i], knots[i-1])
            tail_set.add(knots[-1])
    return len(tail_set)


def task1(text: str):
    lines = text.strip().split("\n")
    return simulate(lines, 2)


def task2(text: str):
    lines = text.strip().split("\n")
    return simulate(lines, 10)


if __name__ == "__main__":
    inp = fts("09in.txt")
    print(task1(inp))
    print(task2(inp))
