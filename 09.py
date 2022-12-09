from collections import namedtuple
Coordinates = namedtuple("Coordinates", "x y")


def file_to_lines(filename):
    with open(filename) as f:
        return f.readlines()


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


inp = file_to_lines("09in.txt")
print(simulate(inp, 2))
print(simulate(inp, 10))
